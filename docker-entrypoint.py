import os
import sys

import uvicorn


def start() -> None:
    uvicorn.run(
        "raydahub.bootstrap.main:make_app",
        factory=True,
        host=os.environ.get("UVICORN_HOST", "0.0.0.0"),
        port=int(os.environ.get("UVICORN_PORT", "8000")),
        workers=int(os.environ.get("UVICORN_WORKERS", "1")),
        root_path=os.environ.get("UVICORN_ROOT_PATH", ""),
        forwarded_allow_ips=os.environ.get("UVICORN_FORWARDED_ALLOW_IPS", "127.0.0.1"),
        server_header=os.environ.get("UVICORN_SERVER_HEADER", "false").lower() == "true",
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: docker-entrypoint.py <command> [args...]")
    if sys.argv[1:] == ["start"]:
        start()
    else:
        os.execvp(sys.argv[1], sys.argv[1:])
