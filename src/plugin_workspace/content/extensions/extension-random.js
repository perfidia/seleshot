Selenium.prototype.doScreen = function(filename, elementsIds) {

	if(!browserVersion.isChrome && !(browserVersion.isIE && !browserVersion.isHTA)) {
		throw new SeleniumError('captureEntirePageScreenshot is only ' + 'implemented for Firefox ("firefox" or "chrome", NOT ' + '"firefoxproxy") and IE non-HTA ("iexploreproxy", NOT "iexplore" ' + 'or "iehta"). The current browser isn\'t one of them!');
	}

	// do or do not ... there is no try

	if(browserVersion.isIE) {
		// targeting snapsIE >= 0.2
		function getFailureMessage(exceptionMessage) {
			var msg = 'Snapsie failed: ';
			if(exceptionMessage) {
				if(exceptionMessage == "Automation server can't create object") {
					msg += 'Is it installed? Does it have permission to run ' + 'as an add-on? See http://snapsie.sourceforge.net/';
				} else {
					msg += exceptionMessage;
				}
			} else {
				msg += 'Undocumented error';
			}
			return msg;
		}

		if( typeof (runOptions) != 'undefined' && runOptions.isMultiWindowMode() == false) {
			// framed mode
			try {
				new Snapsie().saveSnapshot(filename, 'selenium_myiframe');
			} catch (e) {
				throw new SeleniumError(getFailureMessage(e.message));
			}
		} else {
			// multi-window mode
			if(!this.snapsieSrc) {
				// XXX - cache snapsie, and capture the screenshot as a
				// callback. Definitely a hack, because we may be late taking
				// the first screenshot, but saves us from polluting other code
				// for now. I wish there were an easier way to get at the
				// contents of a referenced script!
				var snapsieUrl = (this.browserbot.buttonWindow.location.href).replace(/(Test|Remote)Runner\.html/, 'lib/snapsie.js');
				var self = this;
				new Ajax.Request(snapsieUrl, {
					method : 'get',
					onSuccess : function(transport) {
						self.snapsieSrc = transport.responseText;
						self.doCaptureEntirePageScreenshot(filename, kwargs);
					}
				});
				return;
			}

			// it's going into a string, so escape the backslashes
			filename = filename.replace(/\\/g, '\\\\');

			// this is sort of hackish. We insert a script into the document,
			// and remove it before anyone notices.
			var doc = selenium.browserbot.getDocument();
			var script = doc.createElement('script');
			var scriptContent = this.snapsieSrc + 'try {' + '    new Snapsie().saveSnapshot("' + filename + '");' + '}' + 'catch (e) {' + '    document.getElementById("takeScreenshot").failure =' + '        e.message;' + '}';
			script.id = 'takeScreenshot';
			script.language = 'javascript';
			script.text = scriptContent;
			doc.body.appendChild(script);
			script.parentNode.removeChild(script);
			if(script.failure) {
				throw new SeleniumError(getFailureMessage(script.failure));
			}
		}
		return;
	}

	var grabber = {
		prepareCanvas : function(width, height) {
			var styleWidth = width + 'px';
			var styleHeight = height + 'px';

			var grabCanvas = document.getElementById('screenshot_canvas');
			if(!grabCanvas) {
				// create the canvas
				var ns = 'http://www.w3.org/1999/xhtml';
				grabCanvas = document.createElementNS(ns, 'html:canvas');
				grabCanvas.id = 'screenshot_canvas';
				grabCanvas.style.display = 'none';
				document.documentElement.appendChild(grabCanvas);
			}

			grabCanvas.width = width;
			grabCanvas.style.width = styleWidth;
			grabCanvas.style.maxWidth = styleWidth;
			grabCanvas.height = height;
			grabCanvas.style.height = styleHeight;
			grabCanvas.style.maxHeight = styleHeight;

			return grabCanvas;
		},

		prepareContext : function(canvas, box) {
			var context = canvas.getContext('2d');
			context.clearRect(box.x, box.y, box.width, box.height);
			context.save();
			return context;
		}
	};

	var SGNsUtils = {
		dataUrlToBinaryInputStream : function(dataUrl) {
			var nsIoService = Components.classes["@mozilla.org/network/io-service;1"].getService(Components.interfaces.nsIIOService);
			var channel = nsIoService.newChannelFromURI(nsIoService.newURI(dataUrl, null, null));
			var binaryInputStream = Components.classes["@mozilla.org/binaryinputstream;1"].createInstance(Components.interfaces.nsIBinaryInputStream);

			binaryInputStream.setInputStream(channel.open());
			return binaryInputStream;
		},

		newFileOutputStream : function(nsFile) {
			var writeFlag = 0x02;
			// write only
			var createFlag = 0x08;
			// create
			var truncateFlag = 0x20;
			// truncate
			var fileOutputStream = Components.classes["@mozilla.org/network/file-output-stream;1"].createInstance(Components.interfaces.nsIFileOutputStream);

			// Apparently octal permissions are deprecated, but the suggested alternative is broken in Firefox (and not backwards-compatible from FF 4.0): https://bugzilla.mozilla.org/show_bug.cgi?id=433295
			fileOutputStream.init(nsFile, writeFlag | createFlag | truncateFlag, 0664, null);
			return fileOutputStream;
		},

		writeBinaryInputStreamToFileOutputStream : function(binaryInputStream, fileOutputStream) {
			var numBytes = binaryInputStream.available();
			var bytes = binaryInputStream.readBytes(numBytes);
			fileOutputStream.write(bytes, numBytes);
		}
	};

	// compute dimensions
	var window = this.browserbot.getCurrentWindow();
	var doc = window.document.documentElement;
	var box = {
		x : 0,
		y : 0,
		width : doc.scrollWidth,
		height : doc.scrollHeight
	};
	LOG.debug('computed dimensions');

	var originalBackground = doc.style.background;
	var elm;
	if(elementsIds) {
		var arguments = elementsIds.split(".");

		for(var i = 0; i < arguments.length; i++) {
			LOG.debug('--------element: ' + arguments[i]);
		}
		

	}
	for(var i = 0; i < arguments.length; i++) {
		elementsIds = arguments[i];
		LOG.debug('--------elementPetla: ' + arguments[i]);
		var filenamed = filename + elementsIds + ".jpg";
		LOG.debug('--------filename: ' + filenamed);
		
		
		LOG.debug('element: ' + elm);
		// grab
		var topValue = 0;
		var leftValue = 0;
		var width = 0;
		var height = 0;
		//obj = document.getElementById("hplogo");

		leftValue += this.getElementPositionLeft(elementsIds);
		topValue += this.getElementPositionTop(elementsIds);
		height = this.getElementHeight(elementsIds);
		width = this.getElementWidth(elementsIds);
		//obj = obj.offsetParent;
		//LOG.debug('-------------------: ' + elementD.id);
		//LOG.debug('w: ' + height);
		//LOG.debug('h: ' + width);
		//LOG.debug('goraaaa: ' + elementD.style.width);

		var format = 'png';
		var canvas = grabber.prepareCanvas(width, height);
		var context = grabber.prepareContext(canvas, box);
		context.drawWindow(window, leftValue, topValue, width, height, 'rgb(0, 0, 0)');
		context.restore();
		var dataUrl = canvas.toDataURL("image/" + format);
		LOG.debug('grabbed to canvas');

		doc.style.background = originalBackground;

		// save to file
		var nsFile = Components.classes["@mozilla.org/file/local;1"].createInstance(Components.interfaces.nsILocalFile);
		try {
			nsFile.initWithPath(filenamed);
		} catch (e) {
			if(/NS_ERROR_FILE_UNRECOGNIZED_PATH/.test(e.message)) {
				// try using the opposite file separator

				if(filename.indexOf('/') != -1) {
					filenamed = filenamed.replace(/\//g, '\\');
				} else {
					filenamed = filenamed.replace(/\\/g, '/');
				}
				nsFile.initWithPath(filenamed);
			} else {
				throw e;
			}
		}
		var binaryInputStream = SGNsUtils.dataUrlToBinaryInputStream(dataUrl);
		var fileOutputStream = SGNsUtils.newFileOutputStream(nsFile);
		SGNsUtils.writeBinaryInputStreamToFileOutputStream(binaryInputStream, fileOutputStream);
		fileOutputStream.close();
		LOG.debug('saved to file');
	}
};
