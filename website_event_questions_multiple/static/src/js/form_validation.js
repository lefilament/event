/** @odoo-module **/

import publicWidget from "web.public.widget";
import EventRegistrationForm from "website_event.website_event";

import ajax from "web.ajax";

/// declare widget
// extends from EventRegistrationForm from ocb/addons/website_event/static/src/js/website_event.js
export const EventRegistrationFormWithValidation = EventRegistrationForm.extend({
    /// ------------------------------------------------
    /// WARNING: code duplication for lack of extensibility
    // this is a copy of the on_click function of the parent class
    // which is the one opening the modal with these steps:
    // 1. when clicking on "Register button"
    // 2. look at selection (number of tickets to register)
    // 3. disable the register button if no valid answer (e.g. zero tickets)
    // 4. make an ajax.jsonRpc call to fetch the modal
    // 5. inject the modal inside the page (there can be multiple instances of the modal if the register button is clicked multiple times)
    // the only added behavior is to return the modal class to be able to add form validation logic
    // return value is a Promise<modal | undefined>
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
            _.map(post, function (value, key) {
                return parseInt(value);
            })
        );
        if (!tickets_ordered) {
            $('<div class="alert alert-info"/>')
                .text(_t("Please select at least one ticket."))
                .insertAfter("#registration_form table");
            return new Promise(function () {});
        } else {
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
                $modal.find(".modal-body > div").removeClass("container"); // retrocompatibility - REMOVE ME in master / saas-19
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
                $modal.on("submit", "form", function (ev) {
                    const tokenInput = document.createElement("input");
                    tokenInput.setAttribute("name", "recaptcha_token_response");
                    tokenInput.setAttribute("type", "hidden");
                    tokenInput.setAttribute("value", tokenObj.token);
                    ev.currentTarget.appendChild(tokenInput);
                });
                // THIS IS THE ONLY REAL MODIFICATION
                // return the $modal jQuery object
                return $modal;
            });
        }
    },
    /// ------------------------------------------------

    /**
     * @override
     * override the parent method to replace call to the modified function
     */
    on_click: async function (ev) {
        // get modal from copy (not super())
        const $modal = await this.on_click_parent(ev);
        if ($modal) {
            this.add_validation($modal);
        } else {
            console.log("No modal was added.");
        }
    },

    // this is where I add validation to the form in the modal
    add_validation: function ($modal) {
        console.log("Adding validation to modal.");

        // prevent default
        $modal.on("submit", "form", function (ev) {
            console.log("form submitted");

            // search all check groups with mandatory answers
            $modal
                .find("div.form-check-group.is_mandatory_answer")
                .each(function (index) {
                    console.log("testing group", index);
                    // count number of checkbox
                    let checked_count = 0;
                    $(this)
                        .find(".form-check-input")
                        .each(function () {
                            if ($(this).prop("checked")) checked_count++;
                        });

                    // if zero, prevent default and display message
                    if (checked_count == 0) {
                        console.log("at least one checkbox must be checked");
                        $(this).find(".mandatory-message").removeClass("d-none");
                        ev.preventDefault();
                        ev.stopPropagation();
                    }
                });
        });
    },
});

/// register widget
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
            this.instance = new EventRegistrationFormWithValidation(this); // <--- here we instantiante child widget
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
