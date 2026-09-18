"""数据导入相关路由。"""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.core.response import ok, bad_request, internal_error
from backend.app.core.database import get_db
from backend.app.services.ingest_service import IngestService
from backend.app.preprocess import get_adapter


router = APIRouter(prefix="/data", tags=["data"])


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    """批量上传 CSV/Excel 文件并导入"""
    if not files:
        return bad_request("未上传文件")
    
    if len(files) > 50:
        return bad_request("单次上传文件数不能超过 50 个")
    
    service = IngestService(db)
    results = []
    
    for file in files:
        # 检查文件大小 (10MB)
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            results.append({
                "filename": file.filename,
                "inserted": 0,
                "updated": 0,
                "skipped": 0,
                "bad_rows": [],
                "error": "文件大小超过 10MB 限制"
            })
            continue
        
        # 获取适配器
        try:
            adapter = get_adapter(file.filename)
        except ValueError as e:
            results.append({
                "filename": file.filename,
                "inserted": 0,
                "updated": 0,
                "skipped": 0,
                "bad_rows": [],
                "error": str(e)
            })
            continue
        
        # 处理文件
        try:
            df, bad_rows = adapter.process(content)
            ingest_result = service.ingest(df)
            results.append({
                "filename": file.filename,
                "inserted": ingest_result["inserted"],
                "updated": ingest_result["updated"],
                "skipped": ingest_result["skipped"],
                "bad_rows": [br.to_dict() for br in bad_rows[:10]]  # 只返回前 10 条坏行
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "inserted": 0,
                "updated": 0,
                "skipped": 0,
                "bad_rows": [],
                "error": f"处理失败: {str(e)}"
            })
    
    return ok(results)


@router.post("/sample")
async def load_sample(db: Session = Depends(get_db)):
    """一键加载示例数据"""
    service = IngestService(db)
    try:
        result = service.load_sample()
        return ok(result)
    except Exception as e:
        return internal_error(f"加载示例数据失败: {str(e)}")


@router.post("/clear")
async def clear_data(db: Session = Depends(get_db)):
    """清空所有交通流量数据"""
    service = IngestService(db)
    try:
        count = service.clear_all()
        return ok({"cleared_rows": count})
    except Exception as e:
        return internal_error(f"清空数据失败: {str(e)}")


@router.get("/status")
async def data_status(db: Session = Depends(get_db)):
    """获取数据状态"""
    service = IngestService(db)
    try:
        status = service.get_status()
        return ok(status)
    except Exception as e:
        return internal_error(f"获取状态失败: {str(e)}")
