import argparse
import platform
import subprocess


def get_host_target() -> str:
    system = platform.system()
    if system == "Windows":
        return "windows"
    if system == "Linux":
        return "linux"
    if system == "Darwin":
        return "macos"
    print(f"Не поддерживаемая операционная система: {system}")
    exit()


def validate_target(target: str, host_target: str) -> None:
    if target in {"windows", "linux", "macos"} and target != host_target:
        print(f"Не может собрать {target} на{host_target}")
        exit()

    if target == "ios" and host_target != "macos":
        print("Сборка Ios поддерживается только MacOS")
        exit()

    if target == "android" and host_target not in {"windows", "linux"}:
        print("Сборка Android поддерживается только Windows/Linux")
        exit()


def get_command(target: str) -> list[str]:
    if target == "android":
        return ["uv", "run", "flet", "build", "apk", "-vv"]
    if target == "ios":
        return ["uv", "run", "flet", "build", "ipa", "-vv"]
    return [
        "pyinstaller",
        "--onefile",
        "--hidden-import",
        "my_module",
        "src/main.py",
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Собрать приложение для телефона/пк",
        epilog=(
            "Требования к хосту:\n"
            "  - Windows/linux/MacOS: Может быть собрано только с этой же ОС\n"
            "  - Android: может быть собрано только с Windows/Linux\n"
            "  - Ios: Может быть собран только с MacOS\n\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "цель",
        nargs="?",
        metavar="ЦЕЛЬ",
        choices=["windows", "linux", "macos", "android", "ios"],
        help="Целевая платформа. Стандартно на ОС хоста.",
    )
    args = parser.parse_args()

    host_target = get_host_target()
    target = args.target or host_target

    validate_target(target, host_target)
    command = get_command(target)
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
