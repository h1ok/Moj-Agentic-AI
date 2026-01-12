#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Intent Recognition System
اختبار نظام التعرف على النوايا
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.intent_service import intent_service, IntentType


def test_intent_detection():
    """اختبار التعرف على النوايا"""
    
    print("=" * 80)
    print("🧪 اختبار نظام التعرف على النوايا")
    print("=" * 80)
    
    # أمثلة للاختبار
    test_cases = [
        # إدارة الحسابات
        "أضف حساب تويتر الخاص بي",
        "اعرض حساباتي على انستقرام",
        "احذف حساب فيسبوك",
        
        # إدارة المحتوى
        "انشر تغريدة 'مرحباً بالجميع!'",
        "جدول منشور على انستقرام غداً الساعة 10 صباحاً",
        "اكتب منشور عن الذكاء الاصطناعي",
        
        # التحليلات
        "أرني إحصائيات حسابي على تويتر",
        "كم عدد المتابعين لدي؟",
        "ما هو معدل التفاعل؟",
        
        # التفاعل
        "رد على آخر تعليق",
        "أعجبني آخر منشور",
        
        # عام
        "مرحباً",
        "ساعدني",
        "كيف أستخدم النظام؟",
    ]
    
    print("\n📝 اختبار الأمثلة:\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n{i}. النص: '{text}'")
        print("-" * 80)
        
        result = intent_service.detect_intent(text)
        
        print(f"   ✓ النية: {result.intent.value}")
        print(f"   ✓ الثقة: {result.confidence:.2%}")
        
        if result.platform:
            print(f"   ✓ المنصة: {result.platform.value}")
        
        if result.entities:
            print(f"   ✓ الكيانات المستخرجة:")
            for key, value in result.entities.items():
                print(f"      - {key}: {value}")
    
    print("\n" + "=" * 80)
    print("✅ اكتمل الاختبار!")
    print("=" * 80)


def test_entity_extraction():
    """اختبار استخراج الكيانات"""
    
    print("\n\n" + "=" * 80)
    print("🔍 اختبار استخراج الكيانات")
    print("=" * 80)
    
    test_cases = [
        "انشر على حساب @myaccount",
        "جدول منشور غداً الساعة 15:30",
        "انشر 'هذا محتوى رائع!' على تويتر",
        "أرني إحصائيات آخر 30 يوم",
    ]
    
    for text in test_cases:
        print(f"\n📝 النص: '{text}'")
        result = intent_service.detect_intent(text)
        
        if result.entities:
            print("   الكيانات:")
            for key, value in result.entities.items():
                print(f"   - {key}: {value}")
        else:
            print("   لا توجد كيانات")


def test_suggestions():
    """اختبار الاقتراحات"""
    
    print("\n\n" + "=" * 80)
    print("💡 اختبار الاقتراحات")
    print("=" * 80)
    
    partial_texts = [
        "أضف",
        "انشر",
        "إحصائيات",
    ]
    
    for text in partial_texts:
        print(f"\n📝 نص جزئي: '{text}'")
        suggestions = intent_service.get_intent_suggestions(text)
        
        if suggestions:
            print("   الاقتراحات:")
            for suggestion in suggestions[:3]:
                print(f"   - {suggestion['intent']}: {suggestion['example']}")
        else:
            print("   لا توجد اقتراحات")


if __name__ == "__main__":
    test_intent_detection()
    test_entity_extraction()
    test_suggestions()
    
    print("\n\n" + "=" * 80)
    print("🎉 جميع الاختبارات اكتملت بنجاح!")
    print("=" * 80)
