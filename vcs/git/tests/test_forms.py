from django.test import TestCase
from git.forms import MilestoneForm, LabelForm, IssueForm, CommentForm


class MilestoneFormTest(TestCase):
    def test_title_field_label(self):
        form = MilestoneForm()
        self.assertTrue(
            form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_description_field_label(self):
        form = MilestoneForm()
        self.assertTrue(
            form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_due_date_field_label(self):
        form = MilestoneForm()
        self.assertTrue(
            form.fields['due_date'].label is None or form.fields['due_date'].label == 'Due date')


class LabelFormTest(TestCase):
    def test_title_field_label(self):
        form = LabelForm()
        self.assertTrue(
            form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_description_field_label(self):
        form = LabelForm()
        self.assertTrue(
            form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_color_field_label(self):
        form = LabelForm()
        self.assertTrue(
            form.fields['color'].label is None or form.fields['color'].label == 'Color')


class IssueFormTest(TestCase):
    def test_title_field_label(self):
        form = IssueForm()
        self.assertTrue(
            form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_description_field_label(self):
        form = IssueForm()
        self.assertTrue(
            form.fields['description'].label is None or form.fields['description'].label == 'Description')

    def test_milestone_field_label(self):
        form = IssueForm()
        self.assertTrue(
            form.fields['milestone'].label is None or form.fields['milestone'].label == 'Milestone')

    def test_labels_field_label(self):
        form = IssueForm()
        self.assertTrue(
            form.fields['labels'].label is None or form.fields['labels'].label == 'Labels')

    def test_assignees_field_label(self):
        form = IssueForm()
        self.assertTrue(
            form.fields['assignees'].label is None or form.fields['assignees'].label == 'Assignees')


class CommentFormTest(TestCase):
    def test_title_field_label(self):
        form = CommentForm()
        self.assertTrue(
            form.fields['text'].label is None or form.fields['text'].label == 'Text')
