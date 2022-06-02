from mythic_payloadtype_container.MythicCommandBase import *
from mythic_payloadtype_container.MythicRPC import *
import json
import sys
import base64

class LoadModuleArguments(TaskArguments):
    def __init__(self, command_line, **kwargs):
        super().__init__(command_line, **kwargs)
        self.args = [
            CommandParameter(
                name="file", type=ParameterType.File, description="Zipped library to upload"
            ),
            CommandParameter(
                name="module_name",
                type=ParameterType.String,
                description="Name of module to load, e.g. cryptography"
            )
        ]

    async def parse_arguments(self):
        if len(self.command_line) > 0:
            if self.command_line[0] == "{":
                self.load_args_from_json_string(self.command_line)
            else:
                raise ValueError("Missing JSON arguments")
        else:
            raise ValueError("Missing arguments")


class LoadModuleCommand(CommandBase):
    cmd = "load_module"
    needs_admin = False
    help_cmd = "load_module"
    description = (
        "Upload a python library and load it in-memory"
    )
    version = 1
    author = "@ajpc500"
    attackmapping = []
    argument_class = LoadModuleArguments
    attributes = CommandAttributes(
        supported_python_versions=["Python 2.7", "Python 3.8"],
        supported_os=[SupportedOS.MacOS, SupportedOS.Windows, SupportedOS.Linux ],
    )


    async def create_tasking(self, task: MythicTask) -> MythicTask:
        try:
            file_resp = await MythicRPC().execute(
                "get_file", 
                task_id=task.id,
                file_id=task.args.get_arg("file"),
                get_contents=False
            )
            if file_resp.status == MythicRPCStatus.Success:
                if len(file_resp.response) > 0:
                    task.display_params = f"Loading {task.args.get_arg('module_name')} module into memory"
                elif len(file_resp.response) == 0:
                    raise Exception("Failed to find the named file. Have you uploaded it before? Did it get deleted?")
            else:
                raise Exception("Error from Mythic RPC: " + str(file_resp.error))
        
            file_resp = await MythicRPC().execute("update_file",
                file_id=task.args.get_arg("file"),
                delete_after_fetch=True,
                comment="Uploaded into memory for load_module")
        
        
        except Exception as e:
            raise Exception("Error from Mythic: " + str(sys.exc_info()[-1].tb_lineno) + str(e))
        return task

    async def process_response(self, response: AgentResponse):
        pass
