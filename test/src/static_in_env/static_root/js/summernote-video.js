(function (factory) {
  if (typeof define === 'function' && define.amd) {
    define(['jquery'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('jquery'));
  } else {
    factory(window.jQuery);
  }
}(function ($) {
  if (!$.summernote) {
    return
  }
  $.extend(true, $.summernote.lang, {
    'en-US': {
      /* English */
      videoAttributes: {
        dialogTitle: 'Video',
        tooltip: 'Video',
        pluginTitle: 'Video',
        url: 'Video URL ',
        providers: '(YouTube, Vimeo, Vine, Instagram, DailyMotion or Youku)',
        ok: 'Insert Video'
      }
    }
  });
  $.extend($.summernote.options, {
    videoAttributes: {
      icon: '<i class="note-icon-video"></i>'
    }
  });
  $.extend($.summernote.plugins, {
    'videoAttributes': function (context) {
      var self = this,
        ui = $.summernote.ui,
        $editor = context.layoutInfo.editor,
        $editable = context.layoutInfo.editable,
        options = context.options,
        lang = options.langInfo;
      context.memo('button.videoAttributes', function () {
        var button = ui.button({
          contents: options.videoAttributes.icon,
          tooltip: lang.videoAttributes.tooltip,
          click: function (e) {
            context.invoke('saveRange');
            context.invoke('videoAttributes.show');
          }
        });
        return button.render();
      });
      this.initialize = function () {
        var $container = options.dialogsInBody ? $(document.body) : $editor;
        var body = [
          '<div class="form-group note-form-group row-fluid">',
          '<label class="note-form-label">' + lang.videoAttributes.url + '<small class="text-muted">' + lang.videoAttributes.providers + '</small></label>',
          '<input class="note-video-attributes-href form-control note-form-control note-input" type="text" />',
          '</div>'
        ].join('');
        this.$dialog = ui.dialog({
          title: lang.videoAttributes.dialogTitle,
          body: body,
          footer: '<button href="#" class="btn btn-primary note-video-attributes-btn">' + lang.videoAttributes.ok + '</button>'
        }).render().appendTo($container);
      };
      this.destroy = function () {
        ui.hideDialog(this.$dialog);
        this.$dialog.remove();
      };
      this.bindEnterKey = function ($input, $btn) {
        $input.on('keypress', function (e) {
          if (e.keyCode === 13) $btn.trigger('click');
        });
      };
      this.bindLabels = function () {
        self.$dialog.find('.form-control:first').focus().select();
        self.$dialog.find('label').on('click', function () {
          $(this).parent().find('.form-control:first').focus();
        });
      };
      this.show = function () {
        var $vid = $($editable.data('target'));
        var vidInfo = {
          vidDom: $vid,
          href: $vid.attr('href')
        };
        this.showLinkDialog(vidInfo).then(function (vidInfo) {
          ui.hideDialog(self.$dialog);
          var $vid = vidInfo.vidDom,
            $videoHref = self.$dialog.find('.note-video-attributes-href'),
            url = $videoHref.val(),
            $videoHTML = $('<div/>');
          var ytMatch = url.match(/^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([\w|-]{11})(?:(?:[\?&]t=)(\S+))?$/);
          var igMatch = url.match(/(?:www\.|\/\/)instagram\.com\/p\/(.[a-zA-Z0-9_-]*)/);
          var vMatch = url.match(/\/\/vine\.co\/v\/([a-zA-Z0-9]+)/);
          var vimMatch = url.match(/\/\/(player\.)?vimeo\.com\/([a-z]*\/)*([0-9]{6,11})[?]?.*/);
          var dmMatch = url.match(/.+dailymotion.com\/(video|hub)\/([^_]+)[^#]*(#video=([^_&]+))?/);
          var youkuMatch = url.match(/\/\/v\.youku\.com\/v_show\/id_(\w+)=*\.html/);
          var mp4Match = url.match(/^.+.(mp4|m4v)$/);
          var oggMatch = url.match(/^.+.(ogg|ogv)$/);
          var webmMatch = url.match(/^.+.(webm)$/);
          var ytRegExpForStart = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/;
          var $video;
          if (ytMatch && ytMatch[1].length === 11) {
            var youtubeId = ytMatch[1];
            var start = 0;
            if (typeof ytMatch[2] !== 'undefined') {
              var ytMatchForStart = ytMatch[2].match(ytRegExpForStart);
              if (ytMatchForStart) {
                for (var n = [3600, 60, 1], i = 0, r = n.length; i < r; i++) {
                  start += (typeof ytMatchForStart[i + 1] !== 'undefined' ? n[i] * parseInt(ytMatchForStart[i + 1], 10) : 0);
                }
              } else {
                if (ytMatch[2].match(/^[0-9]*$/)) {
                  start = ytMatch[2]
                }
              }
            }
            $video = $('<iframe>')
              .attr('frameborder', 0)
              .attr('src', '//www.youtube.com/embed/' + youtubeId + (start > 0 ? '?start=' + start : ''))
          } else if (igMatch && igMatch[0].length) {
            $video = $('<iframe>')
              .attr('frameborder', 0)
              .attr('src', 'https://instagram.com/p/' + igMatch[1] + '/embed/')
              .attr('scrolling', 'no')
              .attr('allowtransparency', 'true');
          } else if (vMatch && vMatch[0].length) {
            $video = $('<iframe>')
              .attr('frameborder', 0)
              .attr('src', vMatch[0] + '/embed/simple')
              .attr('class', 'vine-embed');
          } else if (vimMatch && vimMatch[3].length) {
            $video = $('<iframe webkitallowfullscreen mozallowfullscreen allowfullscreen>')
              .attr('frameborder', 0)
              .attr('src', '//player.vimeo.com/video/' + vimMatch[3])
          } else if (dmMatch && dmMatch[2].length) {
            $video = $('<iframe>')
              .attr('frameborder', 0)
              .attr('src', '//www.dailymotion.com/embed/video/' + dmMatch[2])
          } else if (youkuMatch && youkuMatch[1].length) {
            $video = $('<iframe webkitallowfullscreen mozallowfullscreen allowfullscreen>')
              .attr('frameborder', 0)
              .attr('src', '//player.youku.com/embed/' + youkuMatch[1]);
          } else if (mp4Match || oggMatch || webmMatch) {
            $video = $('<video controls>')
              .attr('src', url)
          }
          $video.addClass('note-video-clip');
          $videoHTML.html($video);
          context.invoke('restoreRange');
          context.invoke('editor.insertNode', $videoHTML[0]);
        });
      };
      this.showLinkDialog = function (vidInfo) {
        return $.Deferred(function (deferred) {
          var $videoHref = self.$dialog.find('.note-video-attributes-href');
          $editBtn = self.$dialog.find('.note-video-attributes-btn');
          ui.onDialogShown(self.$dialog, function () {
            context.triggerEvent('dialog.shown');
            $editBtn.click(function (e) {
              e.preventDefault();
              deferred.resolve({
                vidDom: vidInfo.vidDom,
                href: $videoHref.val()
              });
            });
            $videoHref.val(vidInfo.href).focus;
            self.bindEnterKey($editBtn);
            self.bindLabels();
          });
          ui.onDialogHidden(self.$dialog, function () {
            $editBtn.off('click');
            if (deferred.state() === 'pending') deferred.reject();
          });
          ui.showDialog(self.$dialog);
        });
      };
    }
  });
}));