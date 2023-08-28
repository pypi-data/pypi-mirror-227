import uvicorn
from argparse import ArgumentParser

arg = ArgumentParser("AIJobs -- Online tool to VERIFY the collections")
arg.add_argument(
    "--workers", "-w", type=int, default=8, help="The number of workers to use for API"
)
arg.add_argument(
    "--reload",
    "-r",
    action="store_true",
    help="Watch the current folder and reload app when there is any changes",
)
arg.add_argument(
    "--host", "-H", type=str, default="0.0.0.0", help="The IP address to bind to"
)
arg.add_argument("--port", "-p", type=int, default=9000, help="Binding port")
arg.add_argument("--log_level", "-l", type=str, default="info", help="The log level")
args = arg.parse_args()


def cmd():
    uvicorn.run(
        "aijobs.cli.app:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=args.reload,
        workers=args.workers,
        access_log=True,
    )
