from pathlib import Path
from datetime import datetime
import shutil


def collect_errors(raw_logs: Path, output_dir: Path, archive_dir: Path) -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    errors_file = output_dir / f"errors_{timestamp}.log"

    output_dir.mkdir(exist_ok=True)
    archive_dir.mkdir(exist_ok=True)

    with errors_file.open("w", encoding="utf-8") as out:
        for log_file in raw_logs.glob("*.log"):
            for line in log_file.read_text(encoding="utf-8").splitlines():
                if "ERROR" in line:
                    out.write(f"{log_file.name}: {line}\n")
            shutil.move(str(log_file), archive_dir / log_file.name)

    print(f"Erreurs centralisées dans : {errors_file}")
