"""
EduTrack Backend Server
Lightweight REST API & Static File Server powered by Python standard library
Serves API endpoints for student performance, manual entry, Excel bulk imports,
and persists student data in students.json.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
import sys

PORT = 8000
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ADVICE_FILE = os.path.join(DATA_DIR, "advice.json")
DOUBTS_FILE = os.path.join(DATA_DIR, "doubts.json")
THRESHOLDS_FILE = os.path.join(DATA_DIR, "thresholds.json")

# Initial seed data for students if file doesn't exist
DEFAULT_STUDENTS = [
    {
        "id": "ET-2026-401",
        "name": "Aarav Patel",
        "class": "Class 4",
        "section": "A",
        "rollNo": "01",
        "parentName": "Kishorbhai Patel",
        "parentEmail": "parent@edutrack.edu",
        "attendance": 94,
        "avatar": "https://images.unsplash.com/photo-1544717305-2782549b5136?w=150&auto=format&fit=crop&q=80",
        "remarks": "Good curiosity in class activities. Extra daily practice required in multiplication tables.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 58,
                "topics": {
                    "Fractions & Decimals": 65,
                    "Multiplication & Tables": 38,
                    "Division & Remainders": 45,
                    "Geometry & Shapes": 82,
                    "Word Problems & Logic": 60
                }
            },
            "English": {
                "total": 100, "marks": 76,
                "topics": {
                    "Grammar & Tenses": 62,
                    "Vocabulary & Synonyms": 88,
                    "Reading Comprehension": 74,
                    "Spelling & Phonics": 80,
                    "Sentence Formation": 76
                }
            },
            "Gujarati": {
                "total": 100, "marks": 54,
                "topics": {
                    "Kakko & Barakhadi": 78,
                    "Matra Identification & Usage": 36,
                    "Sentence Reading (વાક્ય વાચન)": 62,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 50,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 44
                }
            },
            "Hindi": {
                "total": 100, "marks": 66,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 80,
                    "Matra Application (मात्रा ज्ञान)": 52,
                    "Word Formation (शब्द निर्माण)": 68,
                    "Poem Recitation & Meaning": 82,
                    "Sentence Completion (वाक्य पूर्ति)": 48
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 84,
                "topics": {
                    "Plant Parts & Photosynthesis": 88,
                    "Water Cycle & Conservation": 80,
                    "Living vs Non-Living": 92,
                    "Community Helpers & Roles": 85,
                    "Food, Nutrition & Healthy Habits": 75
                }
            }
        }
    },
    {
        "id": "ET-2026-402",
        "name": "Diya Shah",
        "class": "Class 4",
        "section": "A",
        "rollNo": "02",
        "parentName": "Mehulbhai Shah",
        "parentEmail": "mehul.shah@example.com",
        "attendance": 98,
        "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150&auto=format&fit=crop&q=80",
        "remarks": "Consistently excellent performance across all competencies. Very disciplined and supportive.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 88,
                "topics": {
                    "Fractions & Decimals": 85,
                    "Multiplication & Tables": 92,
                    "Division & Remainders": 86,
                    "Geometry & Shapes": 94,
                    "Word Problems & Logic": 83
                }
            },
            "English": {
                "total": 100, "marks": 86,
                "topics": {
                    "Grammar & Tenses": 84,
                    "Vocabulary & Synonyms": 90,
                    "Reading Comprehension": 88,
                    "Spelling & Phonics": 88,
                    "Sentence Formation": 80
                }
            },
            "Gujarati": {
                "total": 100, "marks": 85,
                "topics": {
                    "Kakko & Barakhadi": 92,
                    "Matra Identification & Usage": 84,
                    "Sentence Reading (વાક્ય વાચન)": 86,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 82,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 81
                }
            },
            "Hindi": {
                "total": 100, "marks": 82,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 88,
                    "Matra Application (मात्रा ज्ञान)": 80,
                    "Word Formation (शब्द निर्माण)": 84,
                    "Poem Recitation & Meaning": 82,
                    "Sentence Completion (वाक्य पूर्ति)": 76
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 90,
                "topics": {
                    "Plant Parts & Photosynthesis": 94,
                    "Water Cycle & Conservation": 88,
                    "Living vs Non-Living": 95,
                    "Community Helpers & Roles": 92,
                    "Food, Nutrition & Healthy Habits": 81
                }
            }
        }
    },
    {
        "id": "ET-2026-403",
        "name": "Jayesh Parmar",
        "class": "Class 4",
        "section": "A",
        "rollNo": "03",
        "parentName": "Sureshbhai Parmar",
        "parentEmail": "suresh.parmar@example.com",
        "attendance": 88,
        "avatar": "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150&auto=format&fit=crop&q=80",
        "remarks": "Good effort in physical and oral activities. Struggles with division and sentence formation.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 52,
                "topics": {
                    "Fractions & Decimals": 45,
                    "Multiplication & Tables": 50,
                    "Division & Remainders": 32,
                    "Geometry & Shapes": 75,
                    "Word Problems & Logic": 58
                }
            },
            "English": {
                "total": 100, "marks": 58,
                "topics": {
                    "Grammar & Tenses": 48,
                    "Vocabulary & Synonyms": 65,
                    "Reading Comprehension": 55,
                    "Spelling & Phonics": 70,
                    "Sentence Formation": 52
                }
            },
            "Gujarati": {
                "total": 100, "marks": 68,
                "topics": {
                    "Kakko & Barakhadi": 82,
                    "Matra Identification & Usage": 64,
                    "Sentence Reading (વાક્ય વાચન)": 72,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 65,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 57
                }
            },
            "Hindi": {
                "total": 100, "marks": 62,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 75,
                    "Matra Application (मात्रा ज्ञान)": 54,
                    "Word Formation (शब्द निर्माण)": 66,
                    "Poem Recitation & Meaning": 70,
                    "Sentence Completion (वाक्य पूर्ति)": 45
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 70,
                "topics": {
                    "Plant Parts & Photosynthesis": 74,
                    "Water Cycle & Conservation": 68,
                    "Living vs Non-Living": 78,
                    "Community Helpers & Roles": 72,
                    "Food, Nutrition & Healthy Habits": 58
                }
            }
        }
    },
    {
        "id": "ET-2026-404",
        "name": "Meera Solanki",
        "class": "Class 4",
        "section": "A",
        "rollNo": "04",
        "parentName": "Dineshbhai Solanki",
        "parentEmail": "dinesh.solanki@example.com",
        "attendance": 92,
        "avatar": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=150&auto=format&fit=crop&q=80",
        "remarks": "Progressing well. Shows high interest in Environmental Studies and creative writing.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 74,
                "topics": {
                    "Fractions & Decimals": 72,
                    "Multiplication & Tables": 78,
                    "Division & Remainders": 68,
                    "Geometry & Shapes": 82,
                    "Word Problems & Logic": 70
                }
            },
            "English": {
                "total": 100, "marks": 78,
                "topics": {
                    "Grammar & Tenses": 74,
                    "Vocabulary & Synonyms": 82,
                    "Reading Comprehension": 78,
                    "Spelling & Phonics": 80,
                    "Sentence Formation": 76
                }
            },
            "Gujarati": {
                "total": 100, "marks": 72,
                "topics": {
                    "Kakko & Barakhadi": 84,
                    "Matra Identification & Usage": 70,
                    "Sentence Reading (વાક્ય વાચન)": 75,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 68,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 63
                }
            },
            "Hindi": {
                "total": 100, "marks": 70,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 80,
                    "Matra Application (मात्रा ज्ञान)": 65,
                    "Word Formation (शब्द निर्माण)": 72,
                    "Poem Recitation & Meaning": 75,
                    "Sentence Completion (वाक्य पूर्ति)": 58
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 86,
                "topics": {
                    "Plant Parts & Photosynthesis": 90,
                    "Water Cycle & Conservation": 84,
                    "Living vs Non-Living": 88,
                    "Community Helpers & Roles": 88,
                    "Food, Nutrition & Healthy Habits": 80
                }
            }
        }
    },
    {
        "id": "ET-2026-405",
        "name": "Rohan Vaghela",
        "class": "Class 4",
        "section": "A",
        "rollNo": "05",
        "parentName": "Bharatbhai Vaghela",
        "parentEmail": "bharat.vaghela@example.com",
        "attendance": 84,
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "remarks": "Urgent remedial attention needed in foundational numeracy and Hindi matras.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 36,
                "topics": {
                    "Fractions & Decimals": 30,
                    "Multiplication & Tables": 28,
                    "Division & Remainders": 32,
                    "Geometry & Shapes": 52,
                    "Word Problems & Logic": 38
                }
            },
            "English": {
                "total": 100, "marks": 52,
                "topics": {
                    "Grammar & Tenses": 42,
                    "Vocabulary & Synonyms": 60,
                    "Reading Comprehension": 48,
                    "Spelling & Phonics": 56,
                    "Sentence Formation": 54
                }
            },
            "Gujarati": {
                "total": 100, "marks": 48,
                "topics": {
                    "Kakko & Barakhadi": 62,
                    "Matra Identification & Usage": 38,
                    "Sentence Reading (વાક્ય વાચન)": 50,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 48,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 42
                }
            },
            "Hindi": {
                "total": 100, "marks": 38,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 55,
                    "Matra Application (मात्रा ज्ञान)": 28,
                    "Word Formation (शब्द निर्माण)": 34,
                    "Poem Recitation & Meaning": 45,
                    "Sentence Completion (वाक्य पूर्ति)": 28
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 62,
                "topics": {
                    "Plant Parts & Photosynthesis": 65,
                    "Water Cycle & Conservation": 58,
                    "Living vs Non-Living": 66,
                    "Community Helpers & Roles": 64,
                    "Food, Nutrition & Healthy Habits": 57
                }
            }
        }
    },
    {
        "id": "ET-2026-501",
        "name": "Pooja Patel",
        "class": "Class 5",
        "section": "A",
        "rollNo": "01",
        "parentName": "Kishorbhai Patel",
        "parentEmail": "parent@edutrack.edu",
        "attendance": 96,
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "remarks": "Diligent student with strong language comprehension. Shows great focus in science projects.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 78,
                "topics": {
                    "Fractions & Decimals": 75,
                    "Multiplication & Tables": 82,
                    "Division & Remainders": 70,
                    "Geometry & Shapes": 86,
                    "Word Problems & Logic": 77
                }
            },
            "English": {
                "total": 100, "marks": 84,
                "topics": {
                    "Grammar & Tenses": 80,
                    "Vocabulary & Synonyms": 86,
                    "Reading Comprehension": 85,
                    "Spelling & Phonics": 88,
                    "Sentence Formation": 81
                }
            },
            "Gujarati": {
                "total": 100, "marks": 80,
                "topics": {
                    "Kakko & Barakhadi": 88,
                    "Matra Identification & Usage": 78,
                    "Sentence Reading (વાક્ય વાચન)": 84,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 78,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 72
                }
            },
            "Hindi": {
                "total": 100, "marks": 76,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 84,
                    "Matra Application (मात्रा ज्ञान)": 72,
                    "Word Formation (शब्द निर्माण)": 78,
                    "Poem Recitation & Meaning": 80,
                    "Sentence Completion (वाक्य पूर्ति)": 66
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 88,
                "topics": {
                    "Plant Parts & Photosynthesis": 92,
                    "Water Cycle & Conservation": 86,
                    "Living vs Non-Living": 90,
                    "Community Helpers & Roles": 88,
                    "Food, Nutrition & Healthy Habits": 84
                }
            }
        }
    },
    {
        "id": "ET-2026-601",
        "name": "Tirth Dave",
        "class": "Class 6",
        "section": "B",
        "rollNo": "07",
        "parentName": "Jigneshbhai Dave",
        "parentEmail": "jignesh.dave@example.com",
        "attendance": 89,
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "remarks": "Good grasp of spatial geometry. Work on word problems needed.",
        "subjects": {
            "Mathematics": {
                "total": 100, "marks": 66,
                "topics": {
                    "Fractions & Decimals": 62,
                    "Multiplication & Tables": 74,
                    "Division & Remainders": 60,
                    "Geometry & Shapes": 78,
                    "Word Problems & Logic": 56
                }
            },
            "English": {
                "total": 100, "marks": 70,
                "topics": {
                    "Grammar & Tenses": 68,
                    "Vocabulary & Synonyms": 74,
                    "Reading Comprehension": 70,
                    "Spelling & Phonics": 72,
                    "Sentence Formation": 66
                }
            },
            "Gujarati": {
                "total": 100, "marks": 65,
                "topics": {
                    "Kakko & Barakhadi": 75,
                    "Matra Identification & Usage": 60,
                    "Sentence Reading (વાક્ય વાચન)": 68,
                    "Vocabulary & Opposites (શબ્દ ભંડોળ)": 64,
                    "Paragraph Comprehension (પરિચ્છેદ સમજ)": 58
                }
            },
            "Hindi": {
                "total": 100, "marks": 62,
                "topics": {
                    "Varnamala (स्वर एवं व्यंजन)": 72,
                    "Matra Application (मात्रा ज्ञान)": 56,
                    "Word Formation (शब्द निर्माण)": 64,
                    "Poem Recitation & Meaning": 66,
                    "Sentence Completion (वाक्य पूर्ति)": 52
                }
            },
            "EVS (Environmental Studies)": {
                "total": 100, "marks": 76,
                "topics": {
                    "Plant Parts & Photosynthesis": 80,
                    "Water Cycle & Conservation": 74,
                    "Living vs Non-Living": 78,
                    "Community Helpers & Roles": 76,
                    "Food, Nutrition & Healthy Habits": 72
                }
            }
        }
    }
]

def load_json(filepath, default_val):
    if not os.path.exists(filepath):
        save_json(filepath, default_val)
        return default_val
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default_val

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# Ensure data file exists
if not os.path.exists(STUDENTS_FILE):
    save_json(STUDENTS_FILE, DEFAULT_STUDENTS)

class EduTrackHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DATA_DIR, **kwargs)

    def end_headers(self):
        # Enable CORS for local API access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, data, status=200):
        response_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    def parse_body(self):
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            try:
                return json.loads(raw_body.decode('utf-8'))
            except Exception as e:
                print(f"Error parsing JSON body: {e}")
                return None
        return None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # API Routes
        if path == "/api/status":
            self.send_json({"status": "ok", "server": "EduTrack Python Backend v1.0", "students_count": len(load_json(STUDENTS_FILE, []))})
            return

        if path == "/api/students":
            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
            # Filter by class if provided
            if "class" in query:
                req_class = query["class"][0]
                students = [s for s in students if s.get("class", "").lower() == req_class.lower()]
            self.send_json(students)
            return

        if path.startswith("/api/students/"):
            student_id = urllib.parse.unquote(path.split("/api/students/")[1])
            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
            match = next((s for s in students if s["id"] == student_id), None)
            if match:
                self.send_json(match)
            else:
                self.send_json({"error": "Student not found"}, status=404)
            return

        if path == "/api/thresholds":
            thresholds = load_json(THRESHOLDS_FILE, {"excellent": 75, "average": 40})
            self.send_json(thresholds)
            return

        if path == "/api/advice":
            advice = load_json(ADVICE_FILE, [])
            self.send_json(advice)
            return

        if path == "/api/doubts":
            doubts = load_json(DOUBTS_FILE, [])
            self.send_json(doubts)
            return

        # Fall back to serving static files
        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_body()

        if path == "/api/students":
            if not body or not body.get("name"):
                self.send_json({"error": "Invalid student data. Name is required."}, status=400)
                return

            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)

            # Auto-assign ID if not provided
            if not body.get("id"):
                existing_nums = []
                for s in students:
                    sid = s.get("id", "")
                    if "-" in sid:
                        last_part = sid.split("-")[-1]
                        if last_part.isdigit():
                            existing_nums.append(int(last_part))
                next_num = max(existing_nums, default=400) + 1
                body["id"] = f"ET-2026-{next_num}"

            # Ensure default structure
            if "subjects" not in body or not body["subjects"]:
                body["subjects"] = {
                    "Mathematics": {"total": 100, "marks": int(body.get("mathMarks", 70)), "topics": {}},
                    "English": {"total": 100, "marks": int(body.get("engMarks", 75)), "topics": {}},
                    "Gujarati": {"total": 100, "marks": int(body.get("gujMarks", 70)), "topics": {}},
                    "Hindi": {"total": 100, "marks": int(body.get("hinMarks", 68)), "topics": {}},
                    "EVS (Environmental Studies)": {"total": 100, "marks": int(body.get("evsMarks", 80)), "topics": {}}
                }

            if not body.get("avatar"):
                body["avatar"] = "https://images.unsplash.com/photo-1544717305-2782549b5136?w=150&auto=format&fit=crop&q=80"

            students.append(body)
            save_json(STUDENTS_FILE, students)
            self.send_json({"success": True, "message": "Student created successfully", "student": body}, status=201)
            return

        if path == "/api/students/bulk":
            if not isinstance(body, list):
                self.send_json({"error": "Body must be an array of student objects"}, status=400)
                return

            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
            imported_count = 0

            for item in body:
                if not item.get("name"):
                    continue

                # Auto ID if missing
                if not item.get("id"):
                    existing_nums = [int(s["id"].split("-")[-1]) for s in students if s.get("id", "").startswith("ET-")]
                    next_num = max(existing_nums, default=400) + 1
                    item["id"] = f"ET-2026-{next_num}"

                # Check if exists by ID -> update, else append
                idx = next((i for i, s in enumerate(students) if s["id"] == item["id"]), -1)
                if idx >= 0:
                    students[idx] = item
                else:
                    students.append(item)
                imported_count += 1

            save_json(STUDENTS_FILE, students)
            self.send_json({"success": True, "importedCount": imported_count, "totalStudents": len(students)})
            return

        if path == "/api/thresholds":
            if body:
                save_json(THRESHOLDS_FILE, body)
                self.send_json({"success": True, "thresholds": body})
            else:
                self.send_json({"error": "No threshold data provided"}, status=400)
            return

        if path == "/api/advice":
            if body:
                advice_list = load_json(ADVICE_FILE, [])
                advice_list.insert(0, body)
                save_json(ADVICE_FILE, advice_list)
                self.send_json({"success": True, "advice": body}, status=201)
            return

        if path == "/api/doubts":
            if body:
                doubts_list = load_json(DOUBTS_FILE, [])
                doubts_list.insert(0, body)
                save_json(DOUBTS_FILE, doubts_list)
                self.send_json({"success": True, "doubt": body}, status=201)
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_body()

        if path.startswith("/api/students/"):
            student_id = urllib.parse.unquote(path.split("/api/students/")[1])
            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
            idx = next((i for i, s in enumerate(students) if s["id"] == student_id), -1)

            if idx == -1:
                self.send_json({"error": "Student not found"}, status=404)
                return

            if body:
                # Merge fields
                for k, v in body.items():
                    students[idx][k] = v
                save_json(STUDENTS_FILE, students)
                self.send_json({"success": True, "student": students[idx]})
            else:
                self.send_json({"error": "No update payload provided"}, status=400)
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/students/"):
            student_id = urllib.parse.unquote(path.split("/api/students/")[1])
            students = load_json(STUDENTS_FILE, DEFAULT_STUDENTS)
            original_len = len(students)
            students = [s for s in students if s["id"] != student_id]

            if len(students) < original_len:
                save_json(STUDENTS_FILE, students)
                self.send_json({"success": True, "message": f"Student {student_id} deleted", "remaining": len(students)})
            else:
                self.send_json({"error": "Student not found"}, status=404)
            return

        self.send_json({"error": "Endpoint not found"}, status=404)

def run():
    handler = EduTrackHandler
    # Enable SO_REUSEADDR so port is immediately freed upon restart
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"==================================================")
        print(f" EduTrack Server running at http://localhost:{PORT}")
        print(f" Web portal:   http://localhost:{PORT}/index.html")
        print(f" Teacher dash: http://localhost:{PORT}/teacher.html")
        print(f" API Base:     http://localhost:{PORT}/api/students")
        print(f" Press Ctrl+C to terminate.")
        print(f"==================================================")
        sys.stdout.flush()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server gracefully...")
            httpd.server_close()

if __name__ == "__main__":
    run()
