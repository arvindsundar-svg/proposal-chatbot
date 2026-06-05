import json
import re
from collections import defaultdict

class ProposalMatcher:
    def __init__(self, knowledge_base_path='knowledge_base.json'):
        with open(knowledge_base_path, 'r') as f:
            self.kb = json.load(f)
        self.sections = self.kb['sections']
        self.proposal = self.kb['proposal']
        self.out_of_scope = self.kb['out_of_scope']
        self._build_index()

    def _build_index(self):
        """Build keyword index for fast lookup."""
        self.keyword_index = defaultdict(list)
        for section in self.sections:
            for keyword in section['keywords']:
                self.keyword_index[keyword.lower()].append(section['id'])
            # Also index words from content
            words = re.findall(r'\b\w+\b', section['content'].lower())
            for word in set(words):
                if len(word) > 4:  # skip short words
                    self.keyword_index[word].append(section['id'])

    STOPWORDS = {'the','is','are','was','were','what','who','where','when','why','how','a','an','of','in','on','at','to','for','with','by','from','about','like','into','through','during','before','after','above','below','between','out','off','over','under','again','further','then','once','here','there','which','while','but','and','or','not','be','do','does','did','will','would','could','should','have','has','had','may','might','shall','can','tell','me','my','minister','prime','tier','dutch','bank','retail','president','chancellor','our','your','us','we','he','she','it','they','them','his','her','its','their','give','get','make','just'}

    def _normalise(self, text):
        """Lowercase, strip punctuation."""
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    def _score_section(self, query_words, section):
        """Score a section against query words."""
        score = 0
        query_text = ' '.join(query_words)

        # Exact keyword phrase match (highest weight)
        for keyword in section['keywords']:
            if keyword.lower() in query_text:
                score += 10
                if keyword.lower() == query_text:
                    score += 5  # exact full match bonus

        # Individual word matches against keywords
        for word in query_words:
            if len(word) < 3 or word in self.STOPWORDS:
                continue
            for keyword in section['keywords']:
                if word in keyword.lower() or keyword.lower() in word:
                    score += 3

        # Content word scoring disabled - keywords only for precision

        return score

    def match(self, query):
        """Match a query to the best section. Returns (section, confidence)."""
        normalised = self._normalise(query)
        query_words = normalised.split()

        if not query_words:
            return None, 0

        # Score all sections
        scores = {}
        for section in self.sections:
            scores[section['id']] = self._score_section(query_words, section)

        best_id = max(scores, key=scores.get)
        best_score = scores[best_id]

        if best_score == 0:
            return None, 0

        # Normalise confidence to 0-1
        confidence = min(best_score / 15.0, 1.0)
        best_section = next(s for s in self.sections if s['id'] == best_id)
        return best_section, confidence

    def get_answer(self, query):
        """Get a formatted answer for a query."""
        section, confidence = self.match(query)

        if confidence < 0.30:
            return {
                'type': 'out_of_scope',
                'answer': "That question falls outside the scope of this proposal. I can answer questions about the programme overview, our approach, team, timeline, investment, technology, AI assurance framework, risk management, why the vendor, and next steps. What would you like to know?",
                'section': None,
                'confidence': confidence
            }

        return {
            'type': 'answer',
            'answer': section['content'],
            'section': section['title'],
            'confidence': confidence
        }

    def get_proposal_meta(self):
        return self.proposal

    def get_suggested_questions(self):
        return [
            "What is this proposal about?",
            "What problem are you solving?",
            "What is the timeline?",
            "How much does it cost?",
            "Who is on the team?",
            "How do you handle AI bias and hallucinations?",
            "What is the ROI?",
            "Why should we choose the vendor?",
            "What are the risks?",
            "What are the next steps?"
        ]
