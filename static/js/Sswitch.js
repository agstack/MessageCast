/*
* Author:  Gopal Joshi
* Website: www.sgeek.org
*/

(function($) {
    $.fn.Sswitch = function(element, options ) {
        this.$element = $(this);
        
        this.options = $.extend({}, $.fn.Sswitch.defaults, {
            state: this.$element.is(":checked"),
            disabled: this.$element.is(":disabled"),
            readonly: this.$element.is("[readonly]"),
            parentClass: this.$element.data("parent"),
            onSwitchChange: element.onSwitchChange
        },options);

        this.$container = $("<div>", {
          "class": (function(_this){
                return function(){
                    var classes;
                    classes = [_this.options.parentClass];
                    classes.push(_this.options.state ? "" + _this.options.parentClass + "-on" : "" + _this.options.parentClass + "-off");
                    if (_this.options.disabled) {
                        classes.push("" + _this.options.parentClass + "-disabled");
                    }
                    if (_this.options.readonly) {
                        classes.push("" + _this.options.parentClass + "-readonly");
                    }
                    if (_this.$element.attr("id")) {
                        classes.push("" + _this.options.parentClass + "-id-" + (_this.$element.attr("id")));
                    }
                    return classes.join(" ");
                };
            })(this)()
        });
        this.$label = $("<span>", {
          html: this.options.labelText,
          "class": "" + this.options.parentClass + "-label"
        });
        this.$container = this.$element.wrap(this.$container).parent();
        this.$element.before(this.$label);
        
        return this.$container.on("click", (function(_this) {
            return function(event) {
                event.preventDefault();
                event.stopPropagation();
                if (_this.options.readonly || _this.options.disabled) {
                  return _this.target;
                }
                _this.options.state = !_this.options.state;
                _this.$element.prop("checked", _this.options.state);
                _this.$container.addClass(_this.options.state ? "" + _this.options.parentClass + "-on" : "" + _this.options.parentClass + "-off").removeClass(_this.options.state ? "" + _this.options.parentClass + "-off" : "" + _this.options.parentClass + "-on");
                _this.options.onSwitchChange.call(_this);
                return _this;
            };
        })(this));
        return this.$element;
    },
    $.fn.Sswitch.defaults = {
        text     : 'Default Title',
        fontsize : 10,
        state: true,
        disabled: false,
        readonly: false,
        parentClass: "s-switch",
        onSwitchChange: function() {}
    };
}(jQuery));