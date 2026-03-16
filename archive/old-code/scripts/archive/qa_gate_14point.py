#!/usr/bin/env python3
"""
Enhanced QA Gate with detailed diagnostics
"""

import re
import json
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

class QAGate:
    def __init__(self):
        self.results = []
        self.issues = defaultdict(int)
        
    def parse_html(self, filepath: str) -> List[Dict]:
        """Extract prospects array from HTML JavaScript"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the prospects array
        match = re.search(r'const prospects = \[(.*?)\];', content, re.DOTALL)
        if not match:
            raise ValueError("Could not find prospects array in HTML")
        
        array_str = '[' + match.group(1) + ']'
        
        # Parse JSON-like structure (JavaScript to JSON conversion)
        array_str = re.sub(r":\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*([,\}])", r': "\1"\2', array_str)
        
        try:
            prospects = json.loads(array_str)
        except json.JSONDecodeError:
            # Fallback: manually parse objects
            prospects = self._manual_parse(match.group(1))
        
        return prospects
    
    def _manual_parse(self, content: str) -> List[Dict]:
        """Manual parsing of JavaScript objects"""
        prospects = []
        objects = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content)
        
        for obj_str in objects:
            prospect = {}
            
            id_match = re.search(r'id:\s*(\d+)', obj_str)
            if id_match:
                prospect['id'] = int(id_match.group(1))
            
            name_match = re.search(r'name:\s*"([^"]*)"', obj_str)
            if name_match:
                prospect['name'] = name_match.group(1)
            
            title_match = re.search(r'title:\s*"([^"]*)"', obj_str)
            if title_match:
                prospect['title'] = title_match.group(1)
            
            company_match = re.search(r'company:\s*"([^"]*)"', obj_str)
            if company_match:
                prospect['company'] = company_match.group(1)
            
            subject_match = re.search(r'subject:\s*"([^"]*)"', obj_str)
            if subject_match:
                prospect['subject'] = subject_match.group(1)
            
            message_match = re.search(r'message:\s*"((?:[^"\\]|\\.)*)"', obj_str)
            if message_match:
                msg = message_match.group(1)
                msg = msg.replace('\\n', '\n')
                prospect['message'] = msg
            
            ab_match = re.search(r'abGroup:\s*"([^"]*)"', obj_str)
            if ab_match:
                prospect['abGroup'] = ab_match.group(1)
            
            if prospect.get('message'):
                prospects.append(prospect)
        
        return prospects
    
    # ========== CHECKS ==========
    
    def check_hard_constraints(self, msg: str) -> List[str]:
        """Check HC1-HC10"""
        issues = []
        
        banned_openings = [
            r'\bi\s+noticed\b',
            r'\bi\s+saw\b',
            r'\bi\s+see\b',
            r'\bi\s+see\s+that\b',
            r'\bseeing\s+that\b'
        ]
        for pattern in banned_openings:
            if re.search(pattern, msg, re.IGNORECASE):
                issues.append("HC1: Uses forbidden opening phrase")
                break
        
        sentences = re.split(r'[.!?]', msg)
        if sentences:
            first_sent = sentences[0].lower()
            if any(term in first_sent for term in ['self-healing', 'self healing', 'ai', 'ml', 'machine learning']):
                if first_sent.find('self') < 20 or first_sent.find('ai') < 20:
                    issues.append("HC2: Opens with AI/self-healing instead of prospect problem")
        
        word_count = len(msg.split())
        if word_count > 120:
            issues.append(f"HC3: {word_count} words (max 120)")
        
        if re.search(r'^\s*[-*]\s+', msg, re.MULTILINE) or re.search(r'^\s*\d+\.\s+', msg, re.MULTILINE):
            issues.append("HC5: Contains bullet-point or numbered-list formatting")
        
        if 'would it be unreasonable' in msg.lower():
            issues.append("HC6: Uses forbidden CTA 'would it be unreasonable'")
        
        if re.search(r'\bphone\b|\bcall\b', msg, re.IGNORECASE):
            if 'phone' in msg.lower() or 'call' in msg.lower():
                issues.append("HC7: Asks for phone number or call")
        
        if 'reaching out' in msg.lower() or 'wanted to connect' in msg.lower():
            issues.append("HC8: Uses forbidden phrase 'reaching out' or 'wanted to connect'")
        
        if 'i figure' in msg.lower() or 'would you like to share' in msg.lower() or 'enough about me' in msg.lower():
            issues.append("HC9: Uses forbidden phrase")
        
        qmark_count = msg.count('?')
        if qmark_count >= 3:
            issues.append(f"HC10: {qmark_count} question marks (max 2)")
        
        return issues
    
    def check_word_count(self, msg: str, touch_num: int = 1) -> Tuple[List[str], int]:
        """CHECK 4: Word count validation"""
        issues = []
        word_count = len(msg.split())
        
        if touch_num == 1:
            if word_count < 80:
                issues.append(f"CHECK4_FAIL: {word_count} words (min 80 for Touch 1)")
            elif word_count > 120:
                issues.append(f"CHECK4_FAIL: {word_count} words (max 120)")
            elif word_count > 99:
                issues.append(f"CHECK4_WARN: {word_count} words (optimal 80-99, acceptable 100-120)")
        
        return issues, word_count
    
    def check_question_count(self, msg: str) -> Tuple[List[str], int]:
        """CHECK 5: Question count (optimal 2)"""
        issues = []
        qmark_count = msg.count('?')
        
        if qmark_count == 0:
            issues.append(f"CHECK5_FAIL: 0 question marks (optimal 2)")
        elif qmark_count == 1:
            issues.append(f"CHECK5_WARN: 1 question mark (optimal 2, data says 34.8%)")
        elif qmark_count > 2:
            issues.append(f"CHECK5_FAIL: {qmark_count} question marks (max 2, optimal 2)")
        
        return issues, qmark_count
    
    def check_evidence(self, msg: str) -> Tuple[List[str], str]:
        """CHECK 7: Evidence check (proof point with number)"""
        issues = []
        evidence = re.search(r'(\d+\s*(?:%|weeks?|days?|minutes?|hours?|months?|x|X|fold))', msg)
        
        if not evidence:
            issues.append("CHECK7_FAIL: No customer proof point with number")
            return issues, None
        
        return issues, evidence.group(1)
    
    def check_phrase_toxicity(self, msg: str) -> List[str]:
        """CHECK 9: Phrase toxicity scan"""
        issues = []
        
        toxic_phrases = [
            (r'\bi\s+noticed\b', 'I noticed'),
            (r'\bi\s+saw\b', 'I saw'),
            (r'\bi\s+see\b', 'I see'),
            (r'\bflaky\s+tests\b', 'flaky tests'),
            (r'\bi\s+figure\b', 'I figure'),
            (r'\bwould\s+you\s+like\s+to\s+share\b', 'would you like to share'),
            (r'\benough\s+about\s+me\b', 'enough about me'),
            (r'\bCI/CD\b', 'CI/CD'),
            (r'\blow\s+code\b', 'low code'),
            (r'\b300%\s+faster\b', '300% faster'),
            (r'\b3[Xx]\s+faster\b', '3X/3x faster'),
            (r'\d+[Xx]\s+faster\b', 'NNNx faster pattern'),
            (r'\breaching\s+out\b', 'reaching out'),
            (r'\bwanted\s+to\s+connect\b', 'wanted to connect'),
            (r'\bseeing\s+that\b', 'seeing that'),
        ]
        
        for pattern, name in toxic_phrases:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                issues.append(f"CHECK9_FAIL: Contains toxic phrase '{name}'")
        
        return issues
    
    def check_cta_validation(self, msg: str) -> Tuple[List[str], bool]:
        """CHECK 10: CTA validation"""
        issues = []
        has_cta = 'what day works' in msg.lower()
        
        if not has_cta:
            issues.append("CHECK10_FAIL: Missing 'what day works' CTA")
        
        return issues, has_cta
    
    def check_hyphen_audit(self, msg: str) -> List[str]:
        """CHECK 11: Hyphen audit (max 1, only compounds)"""
        issues = []
        
        allowed_compounds = [
            'self-healing', 'auto-healing', 'cross-browser',
            'e-prescribing', 'zero-defect'
        ]
        
        msg_lower = msg.lower()
        for compound in allowed_compounds:
            msg_lower = msg_lower.replace(compound, '')
        
        remaining_hyphens = msg_lower.count('-')
        
        if remaining_hyphens > 0:
            issues.append(f"CHECK11_FAIL: Unauthorized hyphen use (found {remaining_hyphens})")
        
        return issues
    
    def check_paragraph_spacing(self, msg: str) -> List[str]:
        """CHECK 12: Paragraph spacing (4+ breaks, max 3 sentences per para)"""
        issues = []
        
        paragraphs = re.split(r'\n\n+|\n(?=\n)', msg)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        if len(paragraphs) < 4:
            issues.append(f"CHECK12_FAIL: {len(paragraphs)} paragraph breaks (min 4)")
        
        for i, para in enumerate(paragraphs):
            sent_count = len(re.split(r'[.!?]', para)) - 1
            if sent_count > 3:
                issues.append(f"CHECK12_FAIL: Paragraph {i+1} has {sent_count} sentences (max 3)")
        
        return issues
    
    def check_em_dash(self, msg: str) -> List[str]:
        """CHECK 14: Em dash check (no — or –)"""
        issues = []
        
        if '—' in msg or '–' in msg:
            issues.append("CHECK14_FAIL: Contains em dash (—) or en dash (–)")
        
        return issues
    
    def check_multiplier_framing(self, msg: str) -> List[str]:
        """CHECK A: No multiplier framing"""
        issues = []
        
        if re.search(r'\d+\s*[Xx]\s+(?:faster|speed|execution|coverage)', msg):
            issues.append("CHECK_A_FAIL: Uses multiplier framing (e.g., '5X faster'). Use reduction framing instead.")
        
        return issues
    
    def check_subject_line(self, subject: str) -> Tuple[List[str], int]:
        """CHECK C: Subject line 3-6 words"""
        issues = []
        word_count = len(subject.split())
        
        if word_count < 3 or word_count > 6:
            issues.append(f"CHECK_C_WARN: Subject line is {word_count} words (optimal 3-6)")
        
        return issues, word_count
    
    def check_banned_closes(self, msg: str) -> List[str]:
        """CHECK D: No banned generic closes"""
        issues = []
        
        banned = [
            r'\bWorth\s+comparing\s+notes\?',
            r'\bWorth\s+a\s+quick\s+chat\?',
            r'\bWould\s+exploring\s+that\s+be\s+worth\s+your\s+time\?',
        ]
        
        for pattern in banned:
            if re.search(pattern, msg, re.IGNORECASE):
                issues.append(f"CHECK_D_FAIL: Uses banned close pattern")
        
        return issues
    
    def check_buzzwords(self, msg: str) -> List[str]:
        """CHECK G: Buzzword check"""
        issues = []
        
        buzzwords = [
            ('velocity', r'\bvelocity\b'),
            ('bottleneck', r'\bbottleneck\b'),
            ('maintenance sprawl', r'\bmaintenance\s+sprawl\b'),
            ('bandwidth', r'\bbandwidth\b'),
            ('leverage', r'\bleverage\b'),
        ]
        
        for name, pattern in buzzwords:
            if re.search(pattern, msg, re.IGNORECASE):
                issues.append(f"CHECK_G_FAIL: Contains buzzword '{name}'")
        
        return issues
    
    def run_qa_on_message(self, prospect: Dict) -> Dict:
        """Run all QA checks on a single message"""
        msg = prospect.get('message', '')
        subject = prospect.get('subject', '')
        
        result = {
            'id': prospect['id'],
            'name': prospect['name'],
            'company': prospect['company'],
            'subject': subject,
            'message': msg,
            'issues': []
        }
        
        # Run all checks
        result['issues'].extend(self.check_hard_constraints(msg))
        issues, word_count = self.check_word_count(msg)
        result['issues'].extend(issues)
        result['word_count'] = word_count
        
        issues, qmark_count = self.check_question_count(msg)
        result['issues'].extend(issues)
        result['qmark_count'] = qmark_count
        
        issues, evidence = self.check_evidence(msg)
        result['issues'].extend(issues)
        result['evidence'] = evidence
        
        result['issues'].extend(self.check_phrase_toxicity(msg))
        
        issues, has_cta = self.check_cta_validation(msg)
        result['issues'].extend(issues)
        result['has_cta'] = has_cta
        
        result['issues'].extend(self.check_hyphen_audit(msg))
        result['issues'].extend(self.check_paragraph_spacing(msg))
        result['issues'].extend(self.check_em_dash(msg))
        result['issues'].extend(self.check_multiplier_framing(msg))
        
        issues, subj_word_count = self.check_subject_line(subject)
        result['issues'].extend(issues)
        result['subject_words'] = subj_word_count
        
        result['issues'].extend(self.check_banned_closes(msg))
        result['issues'].extend(self.check_buzzwords(msg))
        
        # Determine status
        fails = [i for i in result['issues'] if 'FAIL' in i]
        warns = [i for i in result['issues'] if 'WARN' in i]
        
        if fails:
            result['status'] = 'FAIL'
        elif warns:
            result['status'] = 'WARN'
        else:
            result['status'] = 'PASS'
        
        return result
    
    def run_all_qa(self, prospects: List[Dict]):
        """Run QA on all prospects"""
        self.results = []
        for prospect in prospects:
            result = self.run_qa_on_message(prospect)
            self.results.append(result)
    
    def extract_close(self, msg: str) -> str:
        """Extract the closing sentence/paragraph"""
        sentences = re.split(r'(?<=[.!?])\s+', msg.strip())
        if sentences:
            return sentences[-1]
        return msg
    
    def print_results(self):
        """Print detailed results and summary"""
        print("\n" + "="*100)
        print("COMPREHENSIVE QA GATE RESULTS — Batch 8 (Mar 2, 2026)")
        print("="*100 + "\n")
        
        # Detailed results with issue codes
        for result in self.results:
            status_marker = "✓" if result['status'] == 'PASS' else ("!" if result['status'] == 'WARN' else "✗")
            print(f"\n[{status_marker}] ID {result['id']:2d} | {result['name']:25s} | {result['company']:25s} | {result['status']:4s}")
            
            if result['issues']:
                for issue in result['issues']:
                    prefix = "    WARNING:" if "WARN" in issue else "    FAIL:   " if "FAIL" in issue else "    "
                    print(f"{prefix} {issue}")
            else:
                print("    ✓ All checks passed")
        
        # Summary statistics
        print("\n" + "="*100)
        print("SUMMARY STATISTICS")
        print("="*100 + "\n")
        
        pass_count = sum(1 for r in self.results if r['status'] == 'PASS')
        warn_count = sum(1 for r in self.results if r['status'] == 'WARN')
        fail_count = sum(1 for r in self.results if r['status'] == 'FAIL')
        
        print(f"Total Prospects: {len(self.results)}")
        print(f"  PASS: {pass_count} ({100*pass_count//len(self.results)}%)")
        print(f"  WARN: {warn_count} ({100*warn_count//len(self.results)}%)")
        print(f"  FAIL: {fail_count} ({100*fail_count//len(self.results)}%)")
        
        # Most common issues
        print(f"\nMost Common Issues (FAIL/WARN):")
        all_issues = []
        for result in self.results:
            all_issues.extend(result['issues'])
        
        issue_counts = Counter(all_issues)
        for issue, count in issue_counts.most_common(20):
            print(f"  {count:2d}x: {issue}")
        
        # Word count stats
        word_counts = [r['word_count'] for r in self.results]
        print(f"\nWord Count Distribution:")
        print(f"  Average: {sum(word_counts) / len(word_counts):.1f} words")
        print(f"  Min: {min(word_counts)}, Max: {max(word_counts)}")
        print(f"  In optimal range (80-99): {sum(1 for w in word_counts if 80 <= w <= 99)} / {len(word_counts)}")
        print(f"  In acceptable range (100-120): {sum(1 for w in word_counts if 100 <= w <= 120)} / {len(word_counts)}")
        
        # Question mark distribution
        qmark_counts = [r['qmark_count'] for r in self.results]
        print(f"\nQuestion Mark Distribution:")
        qmark_dist = Counter(qmark_counts)
        for q_count in sorted(qmark_dist.keys()):
            print(f"  {q_count} question marks: {qmark_dist[q_count]} messages")
        
        # Subject line word count
        subject_words = [r['subject_words'] for r in self.results]
        print(f"\nSubject Line Word Count Distribution:")
        print(f"  Average: {sum(subject_words) / len(subject_words):.1f} words")
        subject_dist = Counter(subject_words)
        for count in sorted(subject_dist.keys()):
            status = "✓" if 3 <= count <= 6 else "!"
            print(f"  {status} {count} words: {subject_dist[count]} subjects")
        
        # Evidence distribution
        print(f"\nProof Point Distribution:")
        evidence_found = sum(1 for r in self.results if r['evidence'])
        evidence_missing = len(self.results) - evidence_found
        print(f"  With proof point: {evidence_found} / {len(self.results)}")
        print(f"  Missing proof point: {evidence_missing} / {len(self.results)}")
        
        # CTA distribution
        print(f"\nCTA Validation:")
        cta_count = sum(1 for r in self.results if r['has_cta'])
        print(f"  Uses 'what day works': {cta_count} / {len(self.results)}")
        
        print("\n" + "="*100 + "\n")

# Main execution
if __name__ == '__main__':
    qa = QAGate()
    
    # Parse HTML
    print("Parsing HTML file...")
    prospects = qa.parse_html('/sessions/epic-cool-bell/mnt/Work/prospect-outreach-8-2026-03-02.html')
    print(f"Successfully extracted {len(prospects)} prospects\n")
    
    # Run QA
    print("Running 14-point QA gate on all messages...")
    qa.run_all_qa(prospects)
    
    # Print results
    qa.print_results()

