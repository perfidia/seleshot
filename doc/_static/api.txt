API
===

.. function:: create(url):

	Creates an instance of Seleshot object.
	
    :param driver: Web driver for the site
    :type driver: WebDriver
    :returns: Driver of Selenium
    :rtype: WebDriver
	
ScreenShot.create() function contains the following functions and classes:

.. function:: check_url(url):
	
	Check provided url is valid.
	
	:param url: URL - string
	:type url: string
	:returns: Valid URL
	:rtype: string
	:raises: ValueError
	

.. function:: get_web_element_by_id(driver, id):
	
	Get web element by id.

	:param driver: Web Driver
	:type driver: WebDriver
	:param id: id to find WebElement
	:type id: string
	:returns: WebElement from WebDriver
	:rtype: WebElement
	:raises: NoSuchElementException
	

.. function:: get_web_element_by_xpath(driver, xpath):
	
	Get web element by xpath.

	:param driver: Web Driver
	:type driver: WebDriver
	:param xpath: xpath to find WebElement
	:type xpath: string
	:returns: WebElement from WebDriver
	:rtype: WebElement
	:raises: NoSuchElementException
	

.. function:: get_web_element_box_size(web_element):
	
	Get coordinates of the WebElement.

	:param web_element: Element of the web site
	:type web_element: WebElement
	:returns: coordinates of WebElement in box
	:rtype: tuple
	

.. function:: get_screen(driver):
	
	Get screen shoot and save it in a temporary file

	:param driver: Web Driver
	:type driver: WebDriver
	:returns: Screen shot
	:rtype: ImageContainer
	

.. class:: ScreenShot(object):

	.. function:: get_screen(self, url = None):
		
		Get specified screen(s)

		:param url: web page to capture (including http protocol, None to reuse loaded webpage)
		:type url: string
		:returns: Screen shot
		:rtype: ImageContainer
		:raises: Exception
		

.. class:: ImageContainer(object):

    Enumeration of possible positions:

		* MIDDLE
		* INSIDE
		* OUTSIDE
		* BORDER
		* LEFT
		* RIGHT
		* TOP
		* BOTTOM

		Example of usage::

		position = ImageContainer.OUTSIDE | ImageContainer.LEFT


	.. function:: __init__(self, image, driver, cut = False):
		
		Constructor for ImageContainer.

		:param image: In this parameter you can provide Image object or a path to Image
		:type image: Image or string
		:param driver: WebDriver object
		:type driver: WebDriver
		:param cut: True - image was cut one or more times, False - there were not any cut operation
		:type cut: boolean
		:raises: ValueError
		

	.. function:: cut_element(self, id = None, xpath = None):
		
		Cut one element by id or xpath. After this operation you cannot cut more elements.

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:returns: ImageContainer
		:rtype: ImageContainer
		:raises: RuntimeError, ValueError
		

	.. function:: cut_area(self, x = 0, y = 0, height = None, width = None):
		
		Cut area from a given point to a given size (in px)

		:param x: x coordinate for a point
		:type x: integer
		:param y: y coordinate for a point
		:type y: integer
		:param height: height of an area
		:type height: integer or None
		:param width: width of an area
		:type width: integer or None
		:returns: ImageContainer
		:rtype: ImageContainer
		

	.. function:: draw_dot(self, id = None, xpath = None, coordinates = None, padding = 0, color = None, size = None):
		
		For id and xpath:
			Draw a red dot on a given position of a given element.
		For coordinates:
			Draw a red dot in a given point (x, y)

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:param coordinates: coordinates = (x, y) - center of a dot
		:type coordinates: tuple of integers (x, y)
		:param position: position of a dot
		:type position: Position enum
		:param padding: padding between dot and element
		:type padding: tuple of integers (x, y)
		:param color: color of dot
		:type color: color object or string
		:param size: size of dot
		:type size: integer
		:returns: ImageContainer
		:rtype: ImageContainer
		:raises: ValueError
		

	.. function:: draw_frame(self, id = None, xpath = None, coordinates = None, padding = None, color = None, size = None):
		
		For id and xpath:
			Draw a frame around a given element
		For coordinates:
			Draw a frame for a given coordinates

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:param coordinates: coordinates for a frame - coordinates = (x, y, width, height) - middle of a dot
		:type coordinates: tuple of integers - (x, y, width, height)
		:param padding: padding between frame and element
		:type padding: tuple of integers (x, y)
		:param color: color of frame
		:type color: color object or string
		:param size: size of frame (thickness)
		:type size: integer
		:returns: ImageContainer
		:rtype: ImageContainer
		:raises: ValueError
	
	.. function:: draw_image(self, id = None, xpath = None, coordinates = None, position = Position.MIDDLE, padding = (0, 0), filename = None, image = None):	

		For id and xpath:
			Draw an image on a given position of a given element.
		For coordinates:
			Draw an image in a given point (x, y)

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:param coordinates: coordinates = (x, y) - center of an image
		:type coordinates: tuple of integers (x, y)
		:param position: position of an image
		:type position: Position enum
		:param padding: padding between dot and element
		:type padding: tuple of integers (x, y)
		:param filename: filename of the image file
		:type filename: string
		:param image: reference to Image object
		:type image: Image object
		:returns: ImageContainer
		:rtype: ImageContainer
		:raises: ValueError
		
	.. function:: draw_zoom(self, id = None, xpath = None, coordinates = None, position = Position.MIDDLE, padding = (0, 0), zoom = None):
	
		For id and xpath:
			Draw a zoomed image on a given position of a given element.
		For coordinates:
			Draw a zoomed element in a given point (x, y).

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:param coordinates: coordinates = (x, y) - center of a zoomed image
		:type coordinates: tuple of integers (x, y)
		:param position: position of a zoomed image
		:type position: Position enum
		:param padding: padding between dot and element
		:type padding: tuple of integers (x, y)
		:param zoom: zoom size of an element
		:type zoom: integer
		:returns: ImageContainer
		:rtype: ImageContainer
	
	.. function:: draw_blur(self, id = None, xpath = None):

		Blur whole area of the screenshot except a given element.

		:param id: id of a given element
		:type id: string
		:param xpath: xpath of a given element
		:type xpath: string
		:returns: ImageContainer
		:rtype: ImageContainer
		:raises: RuntimeError, ValueError


	.. function:: save(self, filename):
		
		Save to a filename

		:param filename: name of a file
		:type filename: string
		:returns: ImageContainer
		:rtype: ImageContainer


	.. function:: is_cut(self):

        If True, then there is possibility to cut an element.
        If False, then there is not possibility to cut any element.

        :returns: possibility to cut
        :rtype: boolean


    .. function:: __draw_element(self, box, size_x, size_y, remainder_x, remainder_y, position, padding, new_image, image, ellipse = False, color = None):

        Draw element - to draw image set ellipse on False.

        :param box: Box of the element.
        :type box: Tuple with 4 elements
        :param size_x: Size from middle to the border on x
        :type size_x: integer
        :param size_y: Size from middle to the border on y
        :type size_y: integer
        :param remainder_x: Remainder of x scale
        :type remainder_x: integer
        :param remainder_y: Remainder of y scale
        :type remainder_y: integer
        :param position: position of an image
        :type position: Position enum
        :param padding: padding between dot and element
        :type padding: tuple of integers (x, y)
        :param new_image: New image of which will be create.
        :type new_image: Image
        :param image: Image which will be paste into another.
        :type image: Image
        :param ellipse: Draw dot.
        :type ellipse: boolean
        :param color: color of dot
        :type color: color object or string
        :returns: ImageContainer
        :rtype: ImageContainer


	.. function:: close(self):
		
		Close the ImageContainer object		


 
