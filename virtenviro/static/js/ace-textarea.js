/**
 * Created by Petrosyan on 18.02.2016.
 */
(function(){"use strict";jQuery(document).ready(function(a){var b,c,d,e;return d=function(){var a,b,c;for(c="",b="abcdefghijklmnopqrstuvwxyz",a=1;16>a;)c+=b.charAt(Math.floor(Math.random()*b.length)),a++;return"editor-"+c},c=function(b){var c,e;return e=d(),c=a('<div id="'+e+'"></div>'),b.after(c),c},e=function(b,c,d){var e,f;f=c.attr("id"),e=d.getSession().getScreenLength()*d.renderer.lineHeight,b.val(d.getValue()),a("#"+f).css({height:e}),a("#"+f+"-section").css({height:e}),d.resize()},b=function(b){var d,f,g,h,i;return g=b.textarea,g.css({display:"none"}),d=c(g),i=d.attr("id"),h=ace.edit(i),f=a("#"+i),f.css({"margin-bottom":30,"max-width":800}),h.setTheme(b.theme),h.getSession().setUseWrapMode(!0),h.getSession().setMode(b.mode),h.setFontSize(16),h.setValue(g.val(),-1),h.on("change",function(){return e(g,f,h)}),e(g,f,h),a("body").click,h},a.fn.asAceEditor=function(c){var d,e,f;return d=a(this).eq(0),"TEXTAREA"!==d.prop("tagName")?!1:(e={textarea:d,theme:"ace/theme/clouds",mode:"ace/mode/markdown"},f=a.extend(e,c),d.data("ace-editor",b(f)),this)}})}).call(this);
