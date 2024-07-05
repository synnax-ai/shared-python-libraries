from datetime import UTC, datetime


def get_datetime_utc_now_in_iso() -> str:
    return (
        datetime.now(UTC)
        .isoformat(sep="T", timespec="milliseconds")
        .replace("+00:00", "Z")
    )
