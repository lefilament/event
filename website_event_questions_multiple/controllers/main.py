# Copyright 2023 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.exceptions import UserError
from odoo.http import request

from odoo.addons.website_event_questions.controllers.main import WebsiteEvent


class WebsiteEvent(WebsiteEvent):
    def _process_attendees_form(self, event, form_details):
        """Process data posted from the attendee details form.
        Extracts question answers:
        - For questions of type 'multiple_choice', extracting the suggested answer id"""
        registrations = super()._process_attendees_form(event, form_details)

        # list all question_multi_answer with is_mandatory_answer
        mandatory_multiple_general_question_answer_count = {}
        mandatory_multiple_specific_question_ids = set()
        req_filter = (
            lambda q: q.question_type == "multiple_choice" and q.is_mandatory_answer
        )
        for general_question in event.general_question_ids.filtered(req_filter):
            mandatory_multiple_general_question_answer_count[general_question.id] = 0
        for specific_question in event.specific_question_ids.filtered(req_filter):
            mandatory_multiple_specific_question_ids.add(specific_question.id)

        mandatory_multiple_specific_question_answer_count = [
            {i: 0 for i in mandatory_multiple_specific_question_ids}
            for j in range(len(registrations))
        ]

        general_answer_ids = []
        for key, _value in form_details.items():
            # test html input prefix
            if key.startswith("question_multi_answer"):
                _html_input_prefix, registration_index_str, question_answer = key.split(
                    "-"
                )
                registration_index = int(registration_index_str)
                question_id_str, answer_id = question_answer.split("_")
                question_id = int(question_id_str)
                question_sudo = request.env["event.question"].browse(question_id)
                answer_sudo = request.env["event.question.answer"].browse(
                    int(answer_id)
                )
                assert (
                    question_sudo.question_type == "multiple_choice"
                )  # otherwise, html is malformed
                answer_values = {
                    "question_id": question_id,
                    "value_text_box": answer_sudo.name,
                }
                # question with null registration index are general
                if registration_index == 0:
                    general_answer_ids.append((0, 0, answer_values))
                    if question_sudo.is_mandatory_answer:
                        mandatory_multiple_general_question_answer_count[
                            question_id
                        ] += 1
                # question with registration index are specific to one registration
                else:
                    rindex = registration_index - 1  # zero-based array ¹indexing
                    registrations[rindex]["registration_answer_ids"].append(
                        (0, 0, answer_values)
                    )
                    if question_sudo.is_mandatory_answer:
                        mandatory_multiple_specific_question_answer_count[rindex][
                            question_id
                        ] += 1

        # check that answers contain at least one for mandatory question
        # general
        for q, c in mandatory_multiple_general_question_answer_count.items():
            if c == 0:
                raise UserError(
                    "Question "
                    + str(q)
                    + " is mandatory but did not receive an answer."
                )
        # specific
        for r, cc in enumerate(mandatory_multiple_specific_question_answer_count):
            for q, c in cc.items():
                if c == 0:
                    raise UserError(
                        "Question "
                        + str(q)
                        + " is mandatory but did not receive an answer in ticket number "
                        + str(r)
                        + "."
                    )

        # append general question to all items
        for registration in registrations:
            registration["registration_answer_ids"].extend(general_answer_ids)

        return registrations
