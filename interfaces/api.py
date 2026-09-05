# app/interfaces/api/routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import time
import logging
from typing import List

from schemas import (
    AnalysisRequest, BatchRequest,
    AnalysisResponse, BatchResponse,
    AnalysisResult
)
from app.infrastructure.cache import CacheService
from app.core.analyzer import TextAnalyzer  # от Роли 2

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["analysis"])


# === ЗАВИСИМОСТИ ===

def get_cache(request: Request) -> CacheService:
    """Получить сервис кэширования"""
    return request.app.state.cache_service


def get_analyzer(request: Request) -> TextAnalyzer:
    """Получить анализатор текста"""
    return request.app.state.analyzer


# === ЭНДПОИНТЫ ===

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_text(
        request: AnalysisRequest,
        cache: CacheService = Depends(get_cache),
        analyzer: TextAnalyzer = Depends(get_analyzer)
):
    """
    Анализ одного текста

    - Проверяет кэш
    - Если есть — возвращает из кэша
    - Если нет — анализирует и сохраняет в кэш
    """
    start_time = time.time()

    try:
        # 1. Валидация
        if not request.text.strip():
            raise HTTPException(
                status_code=400,
                detail="Текст не может быть пустым"
            )

        if len(request.text) > 10000:
            raise HTTPException(
                status_code=422,
                detail="Текст слишком длинный. Максимум 10000 символов"
            )

        # 2. Проверка кэша
        logger.info(f"📥 Запрос на анализ: {len(request.text)} символов")
        cached_result = cache.get_cached_result(request.text)

        if cached_result:
            logger.info("✅ Ответ из кэша")
            return AnalysisResponse(
                status="success",
                result=cached_result,
                cached=True,
                processing_time=time.time() - start_time
            )

        # 3. Анализ текста (используем анализатор от Роли 2)
        logger.info("🔍 Выполняется анализ...")
        result = analyzer.analyze(request.text)

        # 4. Сохранение в кэш
        cache.set_cached_result(request.text, result)
        logger.info("💾 Результат сохранен в кэш")

        return AnalysisResponse(
            status="success",
            result=result,
            cached=False,
            processing_time=time.time() - start_time
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Ошибка анализа: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.post("/analyze-batch", response_model=BatchResponse)
async def analyze_batch(
        request: BatchRequest,
        cache: CacheService = Depends(get_cache),
        analyzer: TextAnalyzer = Depends(get_analyzer)
):
    """
    Пакетный анализ нескольких текстов

    - Обрабатывает каждый текст с проверкой кэша
    - Возвращает массив результатов
    """
    start_time = time.time()

    try:
        # Валидация
        if not request.texts:
            raise HTTPException(
                status_code=400,
                detail="Список текстов не может быть пустым"
            )

        if len(request.texts) > 100:
            raise HTTPException(
                status_code=422,
                detail="Слишком много текстов. Максимум 100"
            )

        results = []
        cached_status = []

        for i, text in enumerate(request.texts):
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"Текст под номером {i + 1} пустой"
                )

            # Проверка кэша
            cached = cache.get_cached_result(text)
            if cached:
                results.append(cached)
                cached_status.append(True)
                logger.info(f"✅ Текст {i + 1} из кэша")
            else:
                # Анализ
                result = analyzer.analyze(text)
                cache.set_cached_result(text, result)
                results.append(result)
                cached_status.append(False)
                logger.info(f"🔍 Текст {i + 1} проанализирован")

        return BatchResponse(
            status="success",
            results=results,
            cached=cached_status,
            total_time=time.time() - start_time
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Ошибка пакетного анализа: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


@router.get("/cache/stats")
async def cache_stats(
        cache: CacheService = Depends(get_cache)
):
    """Получить статистику кэша"""
    return cache.get_stats()


@router.delete("/cache/clear")
async def clear_cache(
        cache: CacheService = Depends(get_cache),
        text: str = None
):
    """Очистить кэш"""
    success = cache.clear_cache(text)
    if success:
        return {"status": "success", "message": "Кэш очищен"}
    return {"status": "error", "message": "Не удалось очистить кэш"}