from pathlib import Path
import random
import lorem
import names


class DBInsertGeneratorKeys:

    KEY_INSERT_DATA = "insert"

    KEY_FILENAME = "filename"
    KEY_INSERT_NUM = "row_per_insert"
    KEY_INSERT_TOTAL = "row_total"

    KEY_SCHEMA = "schema"
    KEY_TABLE_NAME= "table_name"

    # schema keys
    KEY_NAME = "key"
    KEY_TYPE = "type"
    KEY_RANGE = "range"
    KEY_VALUE = "value"
    KEY_START = "start"
    KEY_STR_TYPE = "str_type"
    KEY_LENGTH = "length"
    KEY_NULL = "allow_null"

    # types
    KEY_TYPE_PRIMARY = "primary"
    KEY_TYPE_INT = "int"
    KEY_TYPE_FLOAT = "float"
    KEY_TYPE_STR = "str"
    KEY_TYPE_TEXT = "text"

    # str type
    KEY_STR_TYPE_FIRSTNAME = "firstname"
    KEY_STR_TYPE_LASTNAME = "lastname"
    KEY_STR_TYPE_FULLNAME = "fullname"
    KEY_STR_TYPE_STR = "str"

    # text length
    KEY_LENGTH_SENTENCE = "sentence"
    KEY_LENGTH_PARAGRAPH = "paragraph"
    KEY_LENGTH_TEXT = "text"

    # registered str
    KEY_NULL_STR = "NULL"
    KEY_REPLACE_IDX = "{idx}"
    KEY_REPLACE_VAL = "{val}"


class DBInsertGenerator:

    SQL_INSERT_TEXT = "INSERT INTO"
    SQL_VALUES_TEXT = "VALUES"

    # file operations
    def load_file(self, filepath: str):
        file_content=""
        with open(filepath, mode="r") as file:
            file_content = file.read()
        return file_content

    def write_file(self, filepath: str, content: str):
        out_path = Path(filepath)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, mode="w") as file:
            file.write(content)

    # column processes
    def process_primary(self, current_idx: int, obj: dict):
        idx = current_idx
        if DBInsertGeneratorKeys.KEY_START in obj:
            idx += int(obj[DBInsertGeneratorKeys.KEY_START])
        return f"{idx}"

    def process_int(self, current_idx: int, obj: dict):
        val = DBInsertGeneratorKeys.KEY_REPLACE_VAL
        if DBInsertGeneratorKeys.KEY_VALUE in obj:
            val = obj[DBInsertGeneratorKeys.KEY_VALUE]

        ret = DBInsertGeneratorKeys.KEY_NULL_STR
        if DBInsertGeneratorKeys.KEY_RANGE in obj:
            range_list = obj[DBInsertGeneratorKeys.KEY_RANGE]
            min_num = min(range_list)
            max_num = max(range_list) + 1
            null_offset = 0
            if (
                DBInsertGeneratorKeys.KEY_NULL in obj and
                obj[DBInsertGeneratorKeys.KEY_NULL] == True
            ):
                null_offset = 1
            ret = random.uniform(min_num,max_num+null_offset)

            if null_offset and ret >= max_num:
                ret = DBInsertGeneratorKeys.KEY_NULL_STR

        return f"{val}".replace(DBInsertGeneratorKeys.KEY_REPLACE_VAL, ret)

    def process_float(self, current_idx: int, obj: dict):
        if DBInsertGeneratorKeys.KEY_VALUE in obj:
            return f"{float(obj[DBInsertGeneratorKeys.KEY_VALUE])}"
        if DBInsertGeneratorKeys.KEY_RANGE in obj:
            range_list = obj[DBInsertGeneratorKeys.KEY_RANGE]
            min_num = min(range_list)
            max_num = max(range_list)
            null_offset = 0
            if (
                DBInsertGeneratorKeys.KEY_NULL in obj and
                obj[DBInsertGeneratorKeys.KEY_NULL] == True
            ):
                null_offset = 1
            ret = random.uniform(min_num,max_num+null_offset)

            if null_offset:
                return f"{ret}" if ret < max_num else DBInsertGeneratorKeys.KEY_NULL_STR
            return f"{ret}"

        return f"{float(current_idx)}"

    def process_str(self, current_idx: int, obj: dict):
        NAMES_TABLE = {
            DBInsertGeneratorKeys.KEY_STR_TYPE_FIRSTNAME: names.get_first_name,
            DBInsertGeneratorKeys.KEY_STR_TYPE_LASTNAME: names.get_last_name,
            DBInsertGeneratorKeys.KEY_STR_TYPE_FULLNAME: names.get_full_name,
        }
        if DBInsertGeneratorKeys.KEY_STR_TYPE in obj:
            str_type = obj[DBInsertGeneratorKeys.KEY_STR_TYPE]

            if str_type != DBInsertGeneratorKeys.KEY_STR_TYPE_STR:
                return f"\"{NAMES_TABLE[str_type]()}\""
            else:
                str_val = obj[DBInsertGeneratorKeys.KEY_VALUE]
                return f"\"{str_val}\"".replace(DBInsertGeneratorKeys.KEY_REPLACE_IDX, str(current_idx))

        return f"\"{NAMES_TABLE[DBInsertGeneratorKeys.KEY_STR_TYPE_FULLNAME]()}\""

    def process_text(self, current_idx: int, obj: dict):
        LOREM_TABLE = {
            DBInsertGeneratorKeys.KEY_LENGTH_PARAGRAPH: lorem.paragraph,
            DBInsertGeneratorKeys.KEY_LENGTH_SENTENCE: lorem.sentence,
            DBInsertGeneratorKeys.KEY_LENGTH_TEXT: lorem.text,
        }

        if DBInsertGeneratorKeys.KEY_LENGTH in obj:
            length = obj[DBInsertGeneratorKeys.KEY_LENGTH]
            return f"\"{LOREM_TABLE[length]()}\""
        return f"\"{LOREM_TABLE[DBInsertGeneratorKeys.KEY_LENGTH_SENTENCE]()}\""

    def process_columns(self, current_idx: int, schema: list):
        PROCESS_TABLE = {
            DBInsertGeneratorKeys.KEY_TYPE_PRIMARY: self.process_primary,
            DBInsertGeneratorKeys.KEY_TYPE_INT: self.process_int,
            DBInsertGeneratorKeys.KEY_TYPE_FLOAT: self.process_float,
            DBInsertGeneratorKeys.KEY_TYPE_STR: self.process_str,
            DBInsertGeneratorKeys.KEY_TYPE_TEXT: self.process_text,
        }

        column_str = "("
        for idx, column in enumerate(schema):
            if idx != 0:
                column_str += ","
            column_str += PROCESS_TABLE[column[DBInsertGeneratorKeys.KEY_TYPE]](current_idx, column)
        column_str += ")"
        return column_str

    # main db insert generation
    def create_db_inserts(self, config_obj: dict):
        PARAM = DBInsertGeneratorKeys
        inserts = config_obj[PARAM.KEY_INSERT_DATA]

        for obj in inserts:
            out_path = Path(obj[PARAM.KEY_FILENAME])
            out_path.parent.mkdir(parents=True, exist_ok=True)

            row_per_insert = obj[PARAM.KEY_INSERT_NUM]
            row_total = obj[PARAM.KEY_INSERT_TOTAL]
            table_name = obj[PARAM.KEY_TABLE_NAME]
            column_data = obj[PARAM.KEY_SCHEMA]
            keys = [ f"`{x[PARAM.KEY_NAME]}`" for x in column_data]
            keys_str = f"({ ','.join(keys) })"
            last_insert_index = row_per_insert - 1
            last_index = row_total - 1

            with open(out_path, mode="w") as file:

                for i in range(row_total):

                    # write sql insert
                    if i % row_per_insert == 0:
                        file.write(f"{self.SQL_INSERT_TEXT} {table_name}\n")
                        file.write(f"{keys_str}\n")
                        file.write(f"{self.SQL_VALUES_TEXT}\n")

                    # write sql values
                    endline = ",\n"
                    if (
                        (i % row_per_insert) == last_insert_index or
                        i == last_index
                    ):
                        print(f"Creating [ {i+1} / {row_total} ] for { table_name }")
                        endline = ";\n\n"
                        
                    file.write(f"{ self.process_columns(i+1, column_data) }{ endline }")


if __name__ == "__main__":
    import yaml
    import argparse

    def get_sample_yml():
        PARAM = DBInsertGeneratorKeys
        return yaml.dump({
            PARAM.KEY_INSERT_DATA: [
                {
                    PARAM.KEY_INSERT_NUM: 10,
                    PARAM.KEY_INSERT_TOTAL: 100,
                    PARAM.KEY_FILENAME: "out/test.sql",
                    PARAM.KEY_TABLE_NAME: "test_table",
                    PARAM.KEY_SCHEMA: [
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_PRIMARY,
                            PARAM.KEY_NAME: "id",
                            PARAM.KEY_START: 10000,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_INT,
                            PARAM.KEY_NAME: "int_as_bool",
                            PARAM.KEY_RANGE: [0,1]
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_INT,
                            PARAM.KEY_NAME: "const_int",
                            PARAM.KEY_VALUE: 777,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_INT,
                            PARAM.KEY_NAME: "range_int",
                            PARAM.KEY_RANGE: [1,7],
                            PARAM.KEY_NULL: True
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_INT,
                            PARAM.KEY_NAME: "custom_range_int",
                            PARAM.KEY_RANGE: [1,7],
                            PARAM.KEY_VALUE: "image_{val}.png",
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_FLOAT,
                            PARAM.KEY_NAME: "const_float",
                            PARAM.KEY_VALUE: 99.99,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_FLOAT,
                            PARAM.KEY_NAME: "range_float",
                            PARAM.KEY_RANGE: [1,7],
                            PARAM.KEY_NULL: True
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_STR,
                            PARAM.KEY_NAME: "email",
                            PARAM.KEY_STR_TYPE: PARAM.KEY_STR_TYPE_STR,
                            PARAM.KEY_VALUE: "seller{idx}@test.com"
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_STR,
                            PARAM.KEY_NAME: "firstname",
                            PARAM.KEY_STR_TYPE: PARAM.KEY_STR_TYPE_FIRSTNAME,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_STR,
                            PARAM.KEY_NAME: "lastname",
                            PARAM.KEY_STR_TYPE: PARAM.KEY_STR_TYPE_LASTNAME,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_STR,
                            PARAM.KEY_NAME: "fullname",
                            PARAM.KEY_STR_TYPE: PARAM.KEY_STR_TYPE_FULLNAME,
                        },
                        {
                            PARAM.KEY_TYPE: PARAM.KEY_TYPE_TEXT,
                            PARAM.KEY_NAME: "sentence",
                            PARAM.KEY_LENGTH: PARAM.KEY_LENGTH_SENTENCE,
                        },
                    ],
                }
            ],
        })

    # argparser
    parser = argparse.ArgumentParser(description="Create db inserts.")
    parser.add_argument("--config", type=str, help="Filepath to config file(yml).")
    parser.add_argument("--create", action='store_true', help="Option to create sample config template.yml")
    args = parser.parse_args()
    
    # create db insert creator instance
    dbig = DBInsertGenerator()

    # create config template sample
    if args.create:
        filename = "config_sample.yml"
        dbig.write_file(filename, get_sample_yml())
        print(f"Created {filename} file.")
        exit(0)

    # check for config file
    if not args.config:
        print("Please insert a config.yml filepath.")
        exit(0)

    # load config file
    data = dbig.load_file(args.config)
    yml_data = yaml.safe_load(data)

    # generate db insert file
    dbig.create_db_inserts(yml_data)
    print("DBInsertCreator completed...")
