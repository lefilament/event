/** @odoo-module **/

/**
 * @copyright: 2025- Le Filament (https://le-filament.com)
 * @copyright: 2004-2015 Odoo S.A.
 * @license: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
 */

import EventRegistrationForm from "website_event.website_event";
import Modal from "web.lib.bootstrap";
import ajax from "web.ajax";
import core from "web.core";
import publicWidget from "web.public.widget";

const _t = core._t;

// Declare widget
// extends from EventRegistrationForm from Odoo addon website_event/static/src/js/website_event.js
export const EventRegistrationFormWithValidation = EventRegistrationForm.extend({
    // ------------------------------------------------
    // WARNING: code duplication for lack of extensibility
    // this is a copy of the on_click function of the parent class
    // which is the one opening the modal with these steps:
    // 1. when clicking on "Register button"
    // 2. look at selection (number of tickets to register)
    // 3. disable the register button if no valid answer (e.g. zero tickets)
    // 4. make an ajax.jsonRpc call to fetch the modal
    // 5. inject the modal inside the page (there can be multiple instances of the modal if the register button is clicked multiple times)
    // the only added behavior is to return the modal class to be able to add form validation logic
    // return value is a Promise<modal | undefined>
    // eslint is applied
    on_click_parent: async function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        var $form = $(ev.currentTarget).closest("form");
        var $button = $(ev.currentTarget).closest('[type="submit"]');
        var post = {};
        $("#registration_form table").siblings(".alert").remove();
        $("#registration_form select").each(function () {
            post[$(this).attr("name")] = $(this).val();
        });
        var tickets_ordered = _.some(
            _.map(post, function (value) {
                return parseInt(value, 10);
            })
        );
        if (!tickets_ordered) {
            $('<div class="alert alert-info"/>')
                .text(_t("Please select at least one ticket."))
                .insertAfter("#registration_form table");
            return new Promise(() => undefined);
        }
        $button.attr("disabled", true);
        var action = $form.data("action") || $form.attr("action");
        var self = this;
        return ajax.jsonRpc(action, "call", post).then(async function (modal) {
            const tokenObj = await self._recaptcha.getToken(
                "website_event_registration"
            );
            if (tokenObj.error) {
                self.displayNotification({
                    type: "danger",
                    title: _t("Error"),
                    message: tokenObj.error,
                    sticky: true,
                });
                $button.prop("disabled", false);
                return false;
            }
            var $modal = $(modal);
            // Retrocompatibility - REMOVE ME in master / saas-19
            $modal.find(".modal-body > div").removeClass("container");
            $modal.appendTo(document.body);
            const modalBS = new Modal($modal[0], {
                backdrop: "static",
                keyboard: false,
            });
            modalBS.show();
            $modal.appendTo("body").modal("show");
            $modal.on("click", ".js_goto_event", function () {
                $modal.modal("hide");
                $button.prop("disabled", false);
            });
            $modal.on("click", ".btn-close", function () {
                $button.prop("disabled", false);
            });
            $modal.on("submit", "form", function (evt) {
                const tokenInput = document.createElement("input");
                tokenInput.setAttribute("name", "recaptcha_token_response");
                tokenInput.setAttribute("type", "hidden");
                tokenInput.setAttribute("value", tokenObj.token);
                evt.currentTarget.appendChild(tokenInput);
            });
            // THIS IS THE ONLY REAL MODIFICATION
            // return the $modal jQuery object
            return $modal;
        });
    },
    // / ------------------------------------------------

    /**
     * @override
     * override the parent method to replace call to the modified function
     */
    on_click: async function (ev) {
        // Get modal from copy (not super())
        const $modal = await this.on_click_parent(ev);
        if ($modal) {
            this.add_validation($modal);
        } else {
            console.log("No modal was added.");
        }
    },

    // This is where I add validation to the form in the modal
    add_validation: function ($modal) {
        console.log("Adding validation to modal.");

        // Prevent default
        $modal.on("submit", "form", function (ev) {
            console.log("form submitted");

            // Search all check groups with mandatory answers
            $modal
                .find("div.form-check-group.is_mandatory_answer")
                .each(function (index) {
                    console.log("testing group", index);
                    // Count number of checkbox
                    let checked_count = 0;
                    $(this)
                        .find(".form-check-input")
                        .each(function () {
                            if ($(this).prop("checked")) checked_count++;
                        });

                    // If zero, prevent default and display message
                    if (checked_count === 0) {
                        console.log("at least one checkbox must be checked");
                        $(this).find(".mandatory-message").removeClass("d-none");
                        ev.preventDefault();
                        ev.stopPropagation();
                    }
                });
        });
    },
});

// Register widget
// (also copied from parent)
publicWidget.registry.EventRegistrationFormWithValidationInstance =
    publicWidget.Widget.extend({
        selector: "#registration_form",

        /**
         * @override
         */
        start: function () {
            console.log("instance start override");
            var def = this._super.apply(this, arguments);
            // Here we instantiante child widget
            this.instance = new EventRegistrationFormWithValidation(this);
            return Promise.all([def, this.instance.attachTo(this.$el)]);
        },
        /**
         * @override
         */
        destroy: function () {
            this.instance.setElement(null);
            this._super.apply(this, arguments);
            this.instance.setElement(this.$el);
        },
    });

console.log("form validation widget registered");
