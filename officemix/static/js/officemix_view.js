function OfficeMixBlock(runtime, element) {
    var iframe = $('iframe', element);
    var player = new playerjs.Player(iframe.get(0));

    var mixUrl = iframe.attr('src');
    var eventUrl = runtime.handlerUrl(element, 'publish_event');

    /**
     * The API returns slides in a 0-based format. Add one to convert into a more human readable format
     */
    function convertSlideIndex(slide) {
        return slide + 1;
    }

    /**
     * Retrieves the current time and slide from the playing Office Mix
     */
    function getCurrentTimeAndSlide (callback) {
        player.getCurrentTime(function (currentTime) {
            player.send({ method: 'getCurrentPage' }, function (currentSlide) {
                callback(currentTime, convertSlideIndex(currentSlide)); 
            });
        });
    }

    

    player.on('ready', function () {
        player.getDuration(function (duration) {
            player.send({ method: 'getPageCount' }, function (totalSlides) {
                var data = {
                    event_type: 'microsoft.office.mix.loaded',
                    url: mixUrl,
                    duration: duration,
                    total_slides: totalSlides
                };

                $.post(eventUrl, JSON.stringify(data));
            });
        });

        player.on('play', function () {
            getCurrentTimeAndSlide(function (currentTime, currentSlide) {
                var data = {
                    event_type: 'microsoft.office.mix.played',
                    url: mixUrl,
                    current_time: currentTime,
                    current_slide: currentSlide
                };

                $.post(eventUrl, JSON.stringify(data));
            });
        });

        player.on('pause', function () {
            getCurrentTimeAndSlide(function (currentTime, currentSlide) {
                var data = {
                    event_type: 'microsoft.office.mix.paused',
                    url: mixUrl,
                    current_time: currentTime,
                    current_slide: currentSlide
                };

                $.post(eventUrl, JSON.stringify(data));
            });
        });

        player.on('ended', function () {
            var data = {
                event_type: 'microsoft.office.mix.stopped',
                url: mixUrl
            };

            $.post(eventUrl, JSON.stringify(data));
        });

        player.on('pageupdate', function (pageUpdateEvent) {
            var data = {
                event_type: 'microsoft.office.mix.slide.loaded',
                url: mixUrl,
                slide: convertSlideIndex(pageUpdateEvent.page) 
            };

            $.post(eventUrl, JSON.stringify(data));
        });
    });
}
