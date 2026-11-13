import unittest
from editorial_render import complete_excerpt, group_sources

class EditorialTests(unittest.TestCase):
    def test_no_character_cut(self):
        text='A complete sentence with a source caveat. '+('Additional grounded context. '*30)
        self.assertEqual(complete_excerpt(text),text.strip())
    def test_no_dangling_next_paragraph(self):
        self.assertEqual(complete_excerpt('A complete paragraph.\n\nHis next argument is here.'),'A complete paragraph. His next argument is here.')
    def test_duplicate_source_preserves_references(self):
        rows=[{'id':'a','url':'https://www.example.com/report/?utm_source=x'}, {'id':'b','url':'https://example.com/report#section'}]
        groups=group_sources(rows)
        self.assertEqual(len(groups),1)
        self.assertEqual([i['id'] for i in groups[0]],['a','b'])
    def test_incomplete_feed_fragment(self):
        self.assertEqual(complete_excerpt('Known fact. The rest is cut…'), 'Known fact. The remaining source excerpt is incomplete.')
        self.assertIn('incomplete',complete_excerpt('https://example.com/cut...', 'A source title'))
    def test_renderer_emits_one_narrative_and_keeps_both_links(self):
        import derive
        from unittest.mock import patch
        rows=[{'id':'one','url':'https://example.com/study','source':'Hacker News'},
              {'id':'two','url':'https://example.com/study','source':'Techmeme'}]
        text='A study result. Its legal limits remain explicit.'
        with patch.object(derive,'story_summary',return_value=text), patch.object(derive,'mark',return_value=''):
            rendered=derive.prose_links(rows)
        self.assertEqual(rendered.count(text),1)
        self.assertIn('one.md',rendered)
        self.assertIn('two.md',rendered)
    def test_distinct_reports_remain(self):
        self.assertEqual(len(group_sources([{'id':'a','url':'https://example.com/a'},{'id':'b','url':'https://example.com/b'}])),2)

if __name__=='__main__':unittest.main()
