/*
 * Navigation menu with accordion effect
 */

$(function() {
		$('#nav > li > a + ul').parent().find('> a').click(function() {
			return false;	// use level-1 nav item for accordion effect only (don't follow URL)
		});

		// collapse all except active menu
		$('#nav > li:not(.selected) > a + ul:not(:has(li.selected))').hide();

		$('#nav li > a').click(function() {
			$(this).find("+ ul").animate({
				height: 'toggle', opacity: 'toggle'
			}, 'normal');
		});
	});
