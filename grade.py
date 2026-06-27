"""
ระบบคิดเกรดอัตโนมัติ - Python CLI Application
Grade Calculation System

ฟลว์แชร์:
START → INPUT SCORE → CHECK SCORE
├─ >= 80 → GRADE A
├─ >= 70 → GRADE B
├─ >= 60 → GRADE C
├─ >= 50 → GRADE D
└─ < 50 → GRADE F
→ SHOW RESULT → END
"""

import json
import os
from datetime import datetime
from pathlib import Path


class GradeCalculator:
    """ระบบคิดเกรดอัตโนมัติ"""
    
    def __init__(self):
        self.data_file = 'grade_history.json'
        self.grades_data = self.load_data()
        
    def load_data(self):
        """โหลดข้อมูลประวัติจากไฟล์"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_data(self):
        """บันทึกข้อมูลประวัติลงไฟล์"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.grades_data, f, ensure_ascii=False, indent=2)
    
    def calculate_grade(self, score):
        """
        คำนวณเกรดจากคะแนน
        
        Args:
            score (float): คะแนน (0-100)
        
        Returns:
            dict: ข้อมูลเกรด
        """
        try:
            score = float(score)
            
            # ตรวจสอบคะแนน
            if score < 0 or score > 100:
                return {
                    'success': False,
                    'error': 'คะแนนต้องอยู่ระหว่าง 0-100'
                }
            
            # กำหนดเกรด
            if score >= 80:
                grade = 'A'
                grade_name = 'ดีเยี่ยม'
                description = 'Excellent'
            elif score >= 70:
                grade = 'B'
                grade_name = 'ดี'
                description = 'Good'
            elif score >= 60:
                grade = 'C'
                grade_name = 'พอใจ'
                description = 'Satisfactory'
            elif score >= 50:
                grade = 'D'
                grade_name = 'ผ่าน'
                description = 'Pass'
            else:
                grade = 'F'
                grade_name = 'ไม่ผ่าน'
                description = 'Fail'
            
            return {
                'success': True,
                'score': score,
                'grade': grade,
                'grade_name': grade_name,
                'description': description
            }
        
        except ValueError:
            return {
                'success': False,
                'error': 'กรุณากรอกตัวเลข'
            }
    
    def add_record(self, name, score, grade):
        """เพิ่มบันทึกลงประวัติ"""
        record = {
            'name': name,
            'score': score,
            'grade': grade,
            'timestamp': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        self.grades_data.append(record)
        self.save_data()
    
    def get_statistics(self, scores_list):
        """
        คำนวณสถิติจากรายชื่อคะแนน
        
        Args:
            scores_list (list): รายชื่อคะแนน
        
        Returns:
            dict: สถิติเกรด
        """
        if not scores_list:
            return None
        
        try:
            scores = [float(s) for s in scores_list]
            
            # ตรวจสอบความถูกต้อง
            if any(s < 0 or s > 100 for s in scores):
                return None
            
            grades = [self.calculate_grade(s)['grade'] for s in scores]
            
            return {
                'total': len(scores),
                'average': sum(scores) / len(scores),
                'max': max(scores),
                'min': min(scores),
                'sum': sum(scores),
                'A': grades.count('A'),
                'B': grades.count('B'),
                'C': grades.count('C'),
                'D': grades.count('D'),
                'F': grades.count('F'),
            }
        except:
            return None
    
    def display_grade_result(self, name, result):
        """แสดงผลการคำนวณเกรด"""
        print("\n" + "=" * 50)
        print("📊 ผลการคำนวณเกรด")
        print("=" * 50)
        print(f"ชื่อ: {name}")
        print(f"คะแนน: {result['score']:.1f}/100")
        print(f"เกรด: {result['grade']} ({result['grade_name']} - {result['description']})")
        print("=" * 50 + "\n")
    
    def display_statistics(self, stats):
        """แสดงสถิติเกรด"""
        print("\n" + "=" * 50)
        print("📈 สถิติเกรด")
        print("=" * 50)
        print(f"จำนวนผู้เรียน: {stats['total']} คน")
        print(f"คะแนนรวม: {stats['sum']:.1f}")
        print(f"คะแนนเฉลี่ย: {stats['average']:.2f}")
        print(f"คะแนนสูงสุด: {stats['max']:.1f}")
        print(f"คะแนนต่ำสุด: {stats['min']:.1f}")
        print("-" * 50)
        print("📊 การแจกแจงเกรด:")
        print(f"  ⭐ เกรด A (ดีเยี่ยม): {stats['A']} คน")
        print(f"  ⭐ เกรด B (ดี): {stats['B']} คน")
        print(f"  ⭐ เกรด C (พอใจ): {stats['C']} คน")
        print(f"  ✓ เกรด D (ผ่าน): {stats['D']} คน")
        print(f"  ✗ เกรด F (ไม่ผ่าน): {stats['F']} คน")
        print("=" * 50 + "\n")


def print_menu():
    """แสดงเมนูหลัก"""
    print("\n" + "=" * 50)
    print("🎓 ระบบคิดเกรด")
    print("=" * 50)
    print("1. 📝 คำนวณเกรดเดี่ยว")
    print("2. 📊 คำนวณสถิติหลายคน")
    print("3. 📋 ดูประวัติ")
    print("4. 🧮 ดูตารางเกรด")
    print("5. 🗑️  ล้างประวัติ")
    print("6. ❌ ออกจากโปรแกรม")
    print("=" * 50)


def show_grade_table():
    """แสดงตารางเกรด"""
    print("\n" + "=" * 60)
    print("📋 ตารางเปรียบเทียบเกรด")
    print("=" * 60)
    print(f"{'ช่วงคะแนน':<15} {'เกรด':<8} {'ความหมาย':<20} {'English':<15}")
    print("-" * 60)
    print(f"{'80 - 100':<15} {'A':<8} {'ดีเยี่ยม':<20} {'Excellent':<15}")
    print(f"{'70 - 79':<15} {'B':<8} {'ดี':<20} {'Good':<15}")
    print(f"{'60 - 69':<15} {'C':<8} {'พอใจ':<20} {'Satisfactory':<15}")
    print(f"{'50 - 59':<15} {'D':<8} {'ผ่าน':<20} {'Pass':<15}")
    print(f"{'0 - 49':<15} {'F':<8} {'ไม่ผ่าน':<20} {'Fail':<15}")
    print("=" * 60 + "\n")


def single_grade_mode(calculator):
    """โหมดคำนวณเกรดเดี่ยว"""
    print("\n📝 โหมดคำนวณเกรดเดี่ยว")
    print("-" * 50)
    
    while True:
        name = input("ชื่อนักเรียน (หรือ 'back' เพื่อกลับ): ").strip()
        if name.lower() == 'back':
            return
        if not name:
            print("❌ กรุณากรอกชื่อ")
            continue
        
        try:
            score_input = input("กรอกคะแนน (0-100): ").strip()
            if score_input.lower() == 'back':
                return
            
            result = calculator.calculate_grade(score_input)
            
            if not result['success']:
                print(f"❌ {result['error']}")
                continue
            
            calculator.display_grade_result(name, result)
            calculator.add_record(name, result['score'], result['grade'])
            print(f"✅ บันทึกลงประวัติแล้ว\n")
            
        except KeyboardInterrupt:
            return


def batch_grade_mode(calculator):
    """โหมดคำนวณสถิติหลายคน"""
    print("\n📊 โหมดคำนวณสถิติหลายคน")
    print("-" * 50)
    print("กรอกคะแนนแต่ละอัน คั่นด้วย Enter (พิมพ์ 'done' เพื่อสิ้นสุด)")
    
    scores = []
    while True:
        try:
            score_input = input(f"คะแนนที่ {len(scores) + 1}: ").strip()
            
            if score_input.lower() == 'done':
                if scores:
                    break
                else:
                    print("❌ กรุณากรอกคะแนนอย่างน้อย 1 อัน")
                    continue
            
            result = calculator.calculate_grade(score_input)
            if result['success']:
                scores.append(result['score'])
                print(f"✅ เพิ่มคะแนน {result['score']} (เกรด {result['grade']})")
            else:
                print(f"❌ {result['error']}")
        
        except KeyboardInterrupt:
            return
    
    stats = calculator.get_statistics(scores)
    if stats:
        calculator.display_statistics(stats)
    else:
        print("❌ เกิดข้อผิดพลาดในการคำนวณ")


def view_history(calculator):
    """ดูประวัติการคำนวณ"""
    if not calculator.grades_data:
        print("\n📭 ยังไม่มีประวัติ")
        return
    
    print("\n" + "=" * 70)
    print("📋 ประวัติการคำนวณ")
    print("=" * 70)
    print(f"{'#':<4} {'ชื่อ':<20} {'คะแนน':<10} {'เกรด':<8} {'เวลา':<20}")
    print("-" * 70)
    
    for i, record in enumerate(calculator.grades_data[-20:], 1):
        print(f"{i:<4} {record['name']:<20} {record['score']:<10.1f} {record['grade']:<8} {record['timestamp']:<20}")
    
    print("=" * 70 + "\n")


def clear_history(calculator):
    """ล้างประวัติ"""
    if not calculator.grades_data:
        print("📭 ไม่มีประวัติให้ล้าง")
        return
    
    confirm = input("⚠️  คุณแน่ใจหรือไม่ว่าต้องการล้างประวัติทั้งหมด? (y/n): ").strip().lower()
    if confirm == 'y':
        calculator.grades_data = []
        calculator.save_data()
        print("✅ ล้างประวัติสำเร็จ")
    else:
        print("❌ ยกเลิก")


def main():
    """โปรแกรมหลัก"""
    calculator = GradeCalculator()
    
    print("\n" + "=" * 50)
    print("🎓 ยินดีต้อนรับสู่ระบบคิดเกรด")
    print("=" * 50)
    print("Grade Calculation System v1.0")
    print("=" * 50 + "\n")
    
    while True:
        try:
            print_menu()
            choice = input("เลือกตัวเลือก (1-6): ").strip()
            
            if choice == '1':
                single_grade_mode(calculator)
            elif choice == '2':
                batch_grade_mode(calculator)
            elif choice == '3':
                view_history(calculator)
            elif choice == '4':
                show_grade_table()
            elif choice == '5':
                clear_history(calculator)
            elif choice == '6':
                print("\n👋 ขอบคุณที่ใช้งาน ลาก่อนครับ\n")
                break
            else:
                print("❌ ตัวเลือกไม่ถูกต้อง กรุณาลองใหม่")
        
        except KeyboardInterrupt:
            print("\n\n👋 ขอบคุณที่ใช้งาน ลาก่อนครับ\n")
            break
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")


if __name__ == '__main__':
    main()
