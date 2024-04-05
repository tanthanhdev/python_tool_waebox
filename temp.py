from bs4 import BeautifulSoup

html = '''
<span slot="prefix">
<pk-badge alt="Arsenal FC" badge-title="Arsenal FC" fallback-image="club-generic-badge" src="https://img.uefa.com/imgml/TP/teams/logos/70x70/52280.png"></pk-badge>
</span>
'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find the pk-badge tag
pk_badge = soup.find('pk-badge')

# Get the value of the src attribute
src_value = pk_badge['src']

print(src_value)
