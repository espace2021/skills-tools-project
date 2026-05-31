from services.sheets_service import (
    get_sheet_records
)


def get_clients():

    return get_sheet_records(
        "clients"
    )