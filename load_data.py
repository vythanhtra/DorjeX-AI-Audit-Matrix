
import pandas as pd

def load_matrix(file_path, sheet="ISO42001_Mapping"):
    """
    Đọc sheet chính từ file Excel chứa bảng mapping kiểm toán.
    :param file_path: Đường dẫn đến file Excel
    :param sheet: Tên sheet cần nạp (mặc định là ISO42001_Mapping)
    :return: pandas.DataFrame
    """
    try:
        xls = pd.ExcelFile(file_path)
        if sheet not in xls.sheet_names:
            raise ValueError(f"❌ Sheet '{sheet}' không tồn tại trong {file_path}. Có sẵn: {xls.sheet_names}")
        df = xls.parse(sheet)
        df.fillna("", inplace=True)
        return df
    except Exception as e:
        raise RuntimeError(f"[load_matrix] Lỗi khi đọc sheet '{sheet}' từ {file_path}: {str(e)}")


def load_all_sheets(file_path):
    """
    Đọc toàn bộ các sheet cần thiết cho hệ thống Audit Matrix
    :return: dict chứa DataFrame cho từng sheet
    """
    required_sheets = [
        "ISO42001_Mapping",
        "KPI_Tracker",
        "Risk_Register",
        "NC_CAPA_Log",
        "Evidence_Matrix",
        "Stakeholder_Needs",
        "Crosswalk",
        "Action_Plan",
        "Dashboard_Visual"
    ]

    try:
        xls = pd.ExcelFile(file_path)
        missing = [s for s in required_sheets if s not in xls.sheet_names]
        if missing:
            raise ValueError(f"❌ Thiếu các sheet sau trong {file_path}: {missing}")

        data = {sheet: xls.parse(sheet).fillna("") for sheet in required_sheets}
        return data
    except Exception as e:
        raise RuntimeError(f"[load_all_sheets] Không thể tải dữ liệu từ {file_path}: {str(e)}")
