import scrapy
import pandas as pd

class TeamGoalsSpider(scrapy.Spider):
    name = 'team_goals'
    start_urls = ['https://www.adamchoi.co.uk/teamgoals/detailed']

    def parse(self, response):
        # Click on the "All matches" button
        yield scrapy.FormRequest.from_response(response, formid='buttons', clickdata={'analytics-event': 'All matches'})

    def after_click(self, response):
        # Select 'Spain' from the dropdown menu
        yield scrapy.FormRequest.from_response(response, formid='dropdowns', formdata={'country': 'Spain'})

    def after_select(self, response):
        # Extract data from the table
        table_rows = response.xpath('//table[@class="table"]//tr')
        all_matches = [row.xpath('.//td//text()').extract() for row in table_rows]

        # Create a pandas DataFrame
        df = pd.DataFrame(all_matches, columns=['Date', 'Home Team', 'Result', 'Away Team', 'Score'])

        # Export DataFrame to CSV
        df.to_csv('football_stats.csv', index=False)
