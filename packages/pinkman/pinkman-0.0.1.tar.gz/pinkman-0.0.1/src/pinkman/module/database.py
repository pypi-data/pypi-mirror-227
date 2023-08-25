# MIT License
#
# Copyright (c) 2023 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import sqlite3

from pinkman.model.message import Message


class Database:
    """Database Class"""

    def connect(self, path):
        """Connect into a database"""
        self.path = path

        self._connection = sqlite3.connect(self.path)

        return self._connection.total_changes

    def migrate(self):
        cursor = self._connection.cursor()

        cursor.execute(
            "CREATE TABLE IF NOT EXISTS message (id TEXT, name TEXT, config TEXT, createdAt TEXT, updatedAt TEXT)"
        )

        cursor.close()

        self._connection.commit()

    def get_message(self, name):
        """Get a row by message name"""
        cursor = self._connection.cursor()

        rows = cursor.execute(
            "SELECT id, name, config, createdAt, updatedAt FROM message WHERE name = '{}'".format(
                name
            )
        ).fetchall()

        cursor.close()

        if len(rows) > 0:
            for row in rows:
                data = json.loads(row[2])

                message = Message(
                    row[0],
                    row[1],
                    data["path"],
                    data["tags"],
                    row[3],
                    row[4],
                )

                return message
        else:
            return None

    def insert_message(self, message):
        """Insert a new row"""
        cursor = self._connection.cursor()

        result = cursor.execute(
            "INSERT INTO message VALUES ('{}', '{}', '{}', datetime('now'), datetime('now'))".format(
                message.id,
                message.name,
                json.dumps(
                    {
                        "path": message.path,
                        "tags": message.tags,
                    }
                ),
            )
        )

        cursor.close()

        self._connection.commit()

        return result.rowcount

    def list_messages(self):
        """List all rows"""
        result = []

        cursor = self._connection.cursor()

        rows = cursor.execute(
            "SELECT id, name, config, createdAt, updatedAt FROM message"
        ).fetchall()

        cursor.close()

        for row in rows:
            data = json.loads(row[2])

            message = Message(
                row[0],
                row[1],
                data["path"],
                data["tags"],
                row[3],
                row[4],
            )

            result.append(message)

        return result

    def delete_message(self, name):
        """Delete a row by message name"""
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM message WHERE name = ?", (name,))
        cursor.close()
        self._connection.commit()
