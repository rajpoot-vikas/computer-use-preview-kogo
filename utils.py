		async def extract_page_content(
			params: PageExtractionAction, browser_session: Browser, page_extraction_llm: BaseChatModel
		):
			
			page = await browser_session.get_current_page()
			
			# Wait for 5 seconds before extracting content
			logger.info('⏱️  Waiting 5 seconds before extracting page content...')
			# await asyncio.sleep(15)  
			await asyncio.sleep(30)  
			
			import markdownify

			strip = ['a', 'img']

			content = markdownify.markdownify(await page.content(), strip=strip)

			# manually append iframe text into the content so it's readable by the LLM (includes cross-origin iframes)
			for iframe in page.frames:
				if iframe.url != page.url and not iframe.url.startswith('data:'):
					content += f'\n\nIFRAME {iframe.url}:\n'
					content += markdownify.markdownify(await iframe.content())

			prompt = 'Your task is to extract the content of the page. You will be given a page and a goal and you should extract all relevant information around this goal from the page. If the goal is vague, summarize the page. Respond in .md format. Extraction goal: {goal}, Page: {page}'
			template = PromptTemplate(input_variables=['goal', 'page'], template=prompt)
			try:
				output = await page_extraction_llm.ainvoke(template.format(goal=params.goal, page=content))
				msg = f'📄  Extracted from page\n: {output.content}\n' 
				logger.info(msg)
				return ActionResult(extracted_content=msg, include_in_memory=True)
			except Exception as e:
				logger.debug(f'Error extracting content: {e}')
				msg = f'📄  Extracted from page\n: {content}\n'
				logger.info(msg)
				return ActionResult(extracted_content=msg)

		# Save as PDF action --------------------------------------------------------------
		@self.registry.action('Save current page as PDF', param_model=SaveAsPDFAction)
		async def save_as_pdf(params: SaveAsPDFAction, browser_session: Browser) -> ActionResult:
			"""Save the current page as PDF using Playwright and return as base64."""
			import base64
			from pathlib import Path
			
			try:
				page = await browser_session.get_current_page()
				
				# Ensure the directory exists
				file_path = Path(params.file_path)
				file_path.parent.mkdir(parents=True, exist_ok=True)
				
				# Default PDF options
				default_options = {
					'format': 'A4',
					'print_background': True,
					'margin': {
						'top': '1cm',
						'right': '1cm',
						'bottom': '1cm',
						'left': '1cm'
					}
				}
				
				# Merge user options with defaults
				pdf_options = {**default_options, **params.options}
				
				# Generate PDF and get binary data
				pdf_bytes = await page.pdf(**pdf_options)
				
				# # Save to file using async I/O
				# try:
				# 	import aiofiles
				# 	async with aiofiles.open(file_path, 'wb') as f:
				# 		await f.write(pdf_bytes)
				# except ImportError:
				# 	# Fallback to synchronous write if aiofiles not available
				# 	with open(file_path, 'wb') as f:
				# 		f.write(pdf_bytes)
				
				# Convert to base64
				pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
				
				msg = f'📄  Successfully saved PDF to: {file_path}'
				logger.info(msg)
				
				return ActionResult(
					extracted_content=pdf_base64,
					include_in_memory=True
				)
				
			except Exception as e:
				error_msg = f'Failed to save PDF: {str(e)}'
				logger.error(error_msg)
				raise Exception(error_msg)





# extracted_json = await extract_structured_data_with_gemini(
#     page_content=content,
#     extraction_goal=params.goal,
#     fields=['parcel_number', 'owner_name', 'tax_amount', 'property_address']
# )