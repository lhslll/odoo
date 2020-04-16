//用 py处理，不用js，此 js 无效
odoo.define('app_base.res_partner_many2one', function (require) {
    'use strict';

    var PartnerField = require('partner.autocomplete.many2one');
    var core = require('web.core');

    var _t = core._t;

    PartnerField.include({
        init: function () {
            this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        _bindAutoComplete: function () {
            this._super.apply(this, arguments);
        },
    });
});
