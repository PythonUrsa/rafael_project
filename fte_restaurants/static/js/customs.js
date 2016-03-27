/* ---------------------------------------------------------- */
/* code developed by Roberto Garcia (rgdesign.org) - dec/2014 */
/* ---------------------------------------------------------- */

/* -------- */

jQuery.noConflict();

function get_window_sizes(q){

	var w = window,
	d = document,
	e = d.documentElement,
	g = d.getElementsByTagName('body')[0],
	x = w.innerWidth || e.clientWidth || g.clientWidth,
	y = w.innerHeight|| e.clientHeight|| g.clientHeight;
	
	if(!q || q == 'w') return x;
	if(q == 'h') return y; 

}

jQuery(document).ready(function(){
	$ = jQuery;
	
	/* toggleCustom */
	var fieldAdjust = $('.field');
	function adjustField(){
		var window_w = get_window_sizes('w');
		var window_h = get_window_sizes('h');
		
		if( window_w > 992){
			fieldAdjust.each(function(){
				var me = $(this); 
				var label_w = me.find('label').innerWidth();
				var me_w = me.innerWidth(); 
				var dif_w = me_w - label_w - 35;
				console.log('label_w: '+label_w);
				console.log('me_w: '+me_w);
				console.log('dif_w: '+dif_w);
				me.find('.selector_wrap').width(dif_w);
			})
		}else{
			fieldAdjust.find('.selector_wrap').width('100%');
			}
	}
	//adjustField();
	 

	/* toggleCustom */
	
	var toggleCustom = $('.custom-toggle');
	
	function openClose(me){
		var toggleItem = $(me.attr('data-target'));
			if( toggleItem.hasClass('closed') ){
				me.addClass('active');
				toggleItem.removeClass('closed');
				adjustField();
				$('.dropdown.open > a').click();
				}else{
				me.removeClass('active');
				toggleItem.addClass('closed'); 
				toggleCustom.each(function(){
					if($(this).attr('data-target') == me.attr('data-target')){
						$(this).removeClass('active');
						}
					}) 
			}
	}
	
	toggleCustom.each(function(){ 
		var me = $(this); 
		me.click(function(e){ 
			openClose(me); 
			return false; 
		})
		
	})
	/* FORM SELECT CUSTOM */
	function open_select(me) {
		elem = me.find('select');
		if (document.createEvent) {
			var e = document.createEvent("MouseEvents");
			e.initMouseEvent("mousedown", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null); 
			elem[0].dispatchEvent(e); 
		} else if (element.fireEvent) { 
			elem[0].fireEvent("onmousedown");
		}
	}
	var select_form = $('select.form-control'); 
	select_form.on('focus',function(){ 
		$(this).parent().find('.tip').addClass('opened')
		})
	select_form.on('blur',function(){
		$(this).parent().find('.tip').removeClass('opened')
		})
	select_form.each(function(){ 
		 
		var me = $(this);
		if(me.hasClass('input-grey')){
			me.wrap('<span class="selector_wrap input-grey"></span>');	 
			}else{
			me.wrap('<span class="selector_wrap"></span>');	 
			}
		
	})
	var selector_wrap = $('span.selector_wrap'); 
	selector_wrap.each(function(){ 
		var me = $(this);
		me.append('<span class="tip fa fa-caret-down"></span>');
		me.click(function(e){ 
			open_select(me); 
			return false;
		}) 
	})
	/* FORM SELECT CUSTOM end */
	
	/* RESIZE */
	function doResize(){
	
		var window_w = get_window_sizes('w');
		var window_h = get_window_sizes('h');
		 
		
		//console.log('Window W: '+window_w);
		if(window_w < 320){
			//console.log('Less than: '+320);
			$('body').addClass("is_mobile_small");
				$('body').removeClass("is_mobile");
				$('body').removeClass("is_tablet");
				$('body').removeClass("is_descktop");
				$('body').removeClass("is_descktop_big");
				$('body').removeClass("is_descktop_bigger");
			}else if(window_w < 768){
				//console.log('Less than: '+640);
				  $('body').addClass("is_mobile");
					$('body').removeClass("is_mobile_small");
					$('body').removeClass("is_tablet");
					$('body').removeClass("is_descktop");
					$('body').removeClass("is_descktop_big");
					$('body').removeClass("is_descktop_bigger");
			}else if (window_w < 992){
				//console.log('Less than: '+960);
				  $('body').addClass("is_tablet");
					$('body').removeClass("is_mobile");
					$('body').removeClass("is_mobile_small");
					$('body').removeClass("is_descktop");
					$('body').removeClass("is_descktop_big");
					$('body').removeClass("is_descktop_bigger");
			}else if (window_w < 1200){
				//console.log('Less than: '+1200);
				  $('body').addClass("is_descktop");
					$('body').removeClass("is_mobile");
					$('body').removeClass("is_tablet");
					$('body').removeClass("is_mobile_small");
					$('body').removeClass("is_descktop_big");
					$('body').removeClass("is_descktop_bigger");
			}else if (window_w < 1680){
				//console.log('Less than: '+1680);
				  $('body').addClass("is_descktop_big");
					$('body').removeClass("is_mobile");
					$('body').removeClass("is_tablet");
					$('body').removeClass("is_mobile_small");
					$('body').removeClass("is_descktop");
					$('body').removeClass("is_descktop_bigger");
			}else if (window_w < 1920){
				//console.log('Less than: '+1920);
				  $('body').addClass("is_descktop_bigger");
					$('body').removeClass("is_mobile");
					$('body').removeClass("is_tablet");
					$('body').removeClass("is_mobile_small");
					$('body').removeClass("is_descktop");
					$('body').removeClass("is_descktop_big");
			}
			
			
			 adjustField();
			 
		
	}
	$(window).resize(function() {
		doResize();
	});
	doResize();
	/* RESIZE end */
	
})