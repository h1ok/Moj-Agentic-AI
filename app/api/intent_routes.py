#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intent API Routes
API endpoints لنظام التعرف على النوايا
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.services.intent_service import intent_service, IntentType, Platform
from app.auth.dependencies import get_current_user
from app.db.models import User

router = APIRouter(prefix="/api/intent", tags=["Intent Recognition"])


class IntentRequest(BaseModel):
    """طلب التعرف على النية"""
    text: str = Field(..., description="النص المدخل من المستخدم")
    context: Optional[Dict[str, Any]] = Field(None, description="سياق إضافي")
    user_id: Optional[int] = Field(None, description="معرف المستخدم")


class IntentResponse(BaseModel):
    """استجابة التعرف على النية"""
    intent: str = Field(..., description="النية المكتشفة")
    confidence: float = Field(..., description="مستوى الثقة (0-1)")
    entities: Dict[str, Any] = Field(..., description="الكيانات المستخرجة")
    platform: Optional[str] = Field(None, description="المنصة المستهدفة")
    raw_text: str = Field(..., description="النص الأصلي")
    timestamp: str = Field(..., description="وقت المعالجة")
    suggestions: Optional[List[str]] = Field(None, description="اقتراحات للإجراءات")


class IntentSuggestionRequest(BaseModel):
    """طلب اقتراحات النوايا"""
    partial_text: str = Field(..., description="نص جزئي")


class IntentSuggestionResponse(BaseModel):
    """استجابة اقتراحات النوايا"""
    suggestions: List[Dict[str, str]] = Field(..., description="قائمة الاقتراحات")


class IntentListResponse(BaseModel):
    """قائمة النوايا المدعومة"""
    intents: List[Dict[str, str]] = Field(..., description="النوايا المدعومة")
    platforms: List[str] = Field(..., description="المنصات المدعومة")


@router.post("/detect", response_model=IntentResponse)
async def detect_intent(
    request: IntentRequest,
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    التعرف على نية المستخدم من النص
    
    يقوم هذا الـ endpoint بتحليل النص المدخل والتعرف على:
    - النية (Intent): ماذا يريد المستخدم أن يفعل
    - الكيانات (Entities): المعلومات المهمة في النص
    - المنصة (Platform): منصة التواصل المستهدفة
    """
    try:
        # التعرف على النية
        result = intent_service.detect_intent(request.text)
        
        # إنشاء اقتراحات للإجراءات
        suggestions = _generate_action_suggestions(result.intent, result.entities)
        
        return IntentResponse(
            intent=result.intent.value,
            confidence=result.confidence,
            entities=result.entities,
            platform=result.platform.value if result.platform else None,
            raw_text=result.raw_text,
            timestamp=result.timestamp.isoformat(),
            suggestions=suggestions
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting intent: {str(e)}"
        )


@router.post("/suggestions", response_model=IntentSuggestionResponse)
async def get_intent_suggestions(request: IntentSuggestionRequest):
    """
    الحصول على اقتراحات للنوايا بناءً على نص جزئي
    
    مفيد للـ autocomplete والمساعدة في كتابة الأوامر
    """
    try:
        suggestions = intent_service.get_intent_suggestions(request.partial_text)
        
        return IntentSuggestionResponse(suggestions=suggestions)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error getting suggestions: {str(e)}"
        )


@router.get("/list", response_model=IntentListResponse)
async def list_supported_intents():
    """
    عرض قائمة بجميع النوايا والمنصات المدعومة
    
    يعرض جميع النوايا التي يمكن للنظام التعرف عليها
    """
    intents = [
        {
            "intent": intent.value,
            "description": intent_service._get_intent_description(intent),
            "category": _get_intent_category(intent)
        }
        for intent in IntentType
        if intent != IntentType.UNKNOWN
    ]
    
    platforms = [platform.value for platform in Platform if platform != Platform.ALL]
    
    return IntentListResponse(
        intents=intents,
        platforms=platforms
    )


@router.post("/batch", response_model=List[IntentResponse])
async def detect_batch_intents(
    requests: List[IntentRequest],
    current_user: Optional[User] = Depends(get_current_user)
):
    """
    التعرف على نوايا متعددة دفعة واحدة
    
    مفيد لمعالجة عدة رسائل أو أوامر في وقت واحد
    """
    try:
        results = []
        
        for req in requests:
            result = intent_service.detect_intent(req.text)
            suggestions = _generate_action_suggestions(result.intent, result.entities)
            
            results.append(IntentResponse(
                intent=result.intent.value,
                confidence=result.confidence,
                entities=result.entities,
                platform=result.platform.value if result.platform else None,
                raw_text=result.raw_text,
                timestamp=result.timestamp.isoformat(),
                suggestions=suggestions
            ))
        
        return results
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error detecting batch intents: {str(e)}"
        )


def _generate_action_suggestions(intent: IntentType, entities: Dict[str, Any]) -> List[str]:
    """إنشاء اقتراحات للإجراءات بناءً على النية"""
    suggestions = []
    
    if intent == IntentType.ADD_ACCOUNT:
        suggestions.append("قم بتوفير بيانات الاعتماد للحساب")
        suggestions.append("اختر المنصة: Twitter, Instagram, Facebook, LinkedIn")
    
    elif intent == IntentType.CREATE_POST:
        if not entities.get("post_content"):
            suggestions.append("قم بكتابة محتوى المنشور")
        if not entities.get("platform"):
            suggestions.append("حدد المنصة للنشر عليها")
        suggestions.append("يمكنك إضافة صور أو فيديو")
    
    elif intent == IntentType.SCHEDULE_POST:
        if not entities.get("schedule_time"):
            suggestions.append("حدد وقت النشر (مثال: غداً الساعة 10 صباحاً)")
        if not entities.get("post_content"):
            suggestions.append("قم بكتابة محتوى المنشور")
    
    elif intent == IntentType.GET_ANALYTICS:
        suggestions.append("اختر الفترة الزمنية: آخر 7 أيام، 30 يوم، 90 يوم")
        suggestions.append("حدد نوع التحليل: إحصائيات عامة، تفاعل، نمو المتابعين")
    
    elif intent == IntentType.LIST_ACCOUNTS:
        suggestions.append("عرض جميع الحسابات المرتبطة")
        suggestions.append("يمكنك تصفية حسب المنصة")
    
    elif intent == IntentType.HELP:
        suggestions.append("يمكنني مساعدتك في:")
        suggestions.append("- إدارة حساباتك على منصات التواصل")
        suggestions.append("- نشر وجدولة المحتوى")
        suggestions.append("- عرض التحليلات والإحصائيات")
        suggestions.append("- أتمتة المهام المتكررة")
    
    return suggestions


def _get_intent_category(intent: IntentType) -> str:
    """تصنيف النية"""
    account_management = [
        IntentType.ADD_ACCOUNT,
        IntentType.REMOVE_ACCOUNT,
        IntentType.LIST_ACCOUNTS,
        IntentType.SWITCH_ACCOUNT
    ]
    
    content_management = [
        IntentType.CREATE_POST,
        IntentType.SCHEDULE_POST,
        IntentType.DELETE_POST,
        IntentType.EDIT_POST
    ]
    
    analytics = [
        IntentType.GET_ANALYTICS,
        IntentType.GET_ENGAGEMENT,
        IntentType.GET_FOLLOWERS
    ]
    
    interaction = [
        IntentType.REPLY_TO_COMMENT,
        IntentType.LIKE_POST,
        IntentType.SHARE_POST
    ]
    
    automation = [
        IntentType.CREATE_AUTOMATION,
        IntentType.MANAGE_AUTOMATION
    ]
    
    if intent in account_management:
        return "account_management"
    elif intent in content_management:
        return "content_management"
    elif intent in analytics:
        return "analytics"
    elif intent in interaction:
        return "interaction"
    elif intent in automation:
        return "automation"
    else:
        return "general"
