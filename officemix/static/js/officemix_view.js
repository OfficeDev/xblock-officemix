function OfficeMixBlock(runtime, element) {
    var iframe = $('iframe', element);
    var player = new playerjs.Player(iframe.get(0));

    var mixUrl = iframe.attr('src');
    var eventUrl = runtime.handlerUrl(element, 'publish_event');

    player.on('ready', function () {
        player.getDuration(function (duration) {
            var data = {
                'event_type': 'xblock.officemix.loaded',
                url: mixUrl,
                duration: duration
            };

            $.post(eventUrl, JSON.stringify(data));
        });

        player.on('play', function () {
            player.getCurrentTime(function (value) {
                var data = {
                    'event_type': 'xblock.officemix.played',
                    url: mixUrl,
                    time: value
                };

                $.post(eventUrl, JSON.stringify(data));
            });
        });

        player.on('pause', function () {
            player.getCurrentTime(function (value) {
                var data = {
                    'event_type': 'xblock.officemix.paused',
                    url: mixUrl,
                    time: value
                };

                $.post(eventUrl, JSON.stringify(data));
            });
        });

        player.on('ended', function () {
            var data = {
                'event_type': 'xblock.officemix.stopped',
                url: mixUrl
            };

            $.post(eventUrl, JSON.stringify(data));
        });
    });
}
