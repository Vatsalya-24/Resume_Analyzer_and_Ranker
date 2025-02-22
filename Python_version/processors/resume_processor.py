import PyPDF2
from docx import Document
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from PyQt6.QtCore import QObject, pyqtSignal
import threading
from datetime import datetime

class ResumeProcessor(QObject):
    analysis_complete = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.files = []
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
    def set_files(self, files):
        self.files = files
    
    def process_resumes(self, requirements):
        results = []
        threads = []
        
        # Create a thread for each resume
        for file in self.files:
            thread = threading.Thread(
                target=self._process_single_resume,
                args=(file, requirements, results)
            )
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
            
        # Sort results by score
        results.sort(key=lambda x: x['score'], reverse=True)
        self.analysis_complete.emit(results)
    
    def _process_single_resume(self, file_path, requirements, results):
        text = self._extract_text(file_path)
        if not text:
            return
            
        # Extract information
        name = self._extract_name(text)
        skills = self._extract_skills(text)
        experience = self._extract_experience(text)
        score = self._calculate_match_score(text, requirements)
        
        # Calculate weighted score based on experience
        experience_weight = 0.3
        skills_weight = 0.7
        weighted_score = (score * skills_weight) + (min(experience, 10) * 10 * experience_weight)
        
        results.append({
            'name': name,
            'skills': skills,
            'experience': experience,
            'score': weighted_score
        })
    
    def _extract_text(self, file_path):
        try:
            if file_path.endswith('.pdf'):
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
            else:  # docx
                doc = Document(file_path)
                text = " ".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return ""
    
    def _extract_name(self, text):
        # Simple name extraction - first line or first capitalized words
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.isupper():  # Avoid headers
                words = line.split()
                if len(words) >= 2 and all(w[0].isupper() for w in words):
                    return line
        return "Unknown"
    
    def _extract_skills(self, text):
        # Common programming languages and technologies
        skill_patterns = [
            'Python', 'Java', 'JavaScript', 'C\+\+', 'SQL', 'React',
            'Angular', 'Node\.js', 'Docker', 'AWS', 'Azure', 'Git',
            'Machine Learning', 'AI', 'Data Science'
        ]
        found_skills = []
        for skill in skill_patterns:
            if re.search(skill, text, re.IGNORECASE):
                found_skills.append(skill)
        return found_skills
    
    def _extract_experience(self, text):
        # First try to find the "Experience" or "Work Experience" section
        experience_headers = [
            r'EXPERIENCE',
            r'WORK EXPERIENCE',
            r'PROFESSIONAL EXPERIENCE',
            r'EMPLOYMENT HISTORY'
        ]
        
        text_lines = text.split('\n')
        experience_section = ""
        in_experience_section = False
        
        for line in text_lines:
            # Check if we've hit an experience section header
            if any(re.search(header, line.upper()) for header in experience_headers):
                in_experience_section = True
                continue
            # Check if we've hit the next section (usually in caps)
            elif in_experience_section and line.isupper() and len(line.strip()) > 10:
                break
            elif in_experience_section:
                experience_section += line + "\n"
        
        # Look for date patterns in the experience section
        date_patterns = [
            r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
            r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|'
            r'Dec(?:ember)?)[,]?\s+(\d{4})',  # Month Year
            r'(\d{1,2})[/-](\d{4})',  # MM/YYYY or M/YYYY
            r'\b(\d{4})\b'  # Just year
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, experience_section, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:  # Month Year format
                    month = match.group(1)
                    year = int(match.group(2))
                    dates.append(year)
                else:  # Year only format
                    year = int(match.group(1))
                    dates.append(year)
        
        if dates:
            # Calculate total experience
            if len(dates) >= 2:
                earliest_date = min(dates)
                latest_date = max(dates)
                total_years = latest_date - earliest_date
                
                # If the latest date is in the future, use current year
                current_year = datetime.now().year
                if latest_date > current_year:
                    total_years = current_year - earliest_date
                    
                return total_years
        
        # Fallback: Look for explicit mentions of years of experience
        experience_patterns = [
            r'(\d+)\+?\s*years?(?:\s+of)?\s+experience',
            r'experience\s*(?:of|:)?\s*(\d+)\+?\s*years?'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1))
            
        return 0
    
    def _calculate_match_score(self, resume_text, requirements):
        # Tokenize and clean text
        resume_tokens = set(word_tokenize(resume_text.lower()))
        req_tokens = set(word_tokenize(requirements.lower()))
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        resume_tokens = resume_tokens - stop_words
        req_tokens = req_tokens - stop_words
        
        # Calculate match score
        matching_tokens = resume_tokens.intersection(req_tokens)
        score = (len(matching_tokens) / len(req_tokens)) * 100
        return score 