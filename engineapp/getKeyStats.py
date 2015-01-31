import sys, math
import urllib2
from BeautifulSoup import BeautifulSoup
import logging


# Download the Key Statistics given a ticker symbol
# Return Key Statistics and list of Keys
def getKeyStats(ticker, DEBUG):
  # Download Key Stats from http://finance.yahoo.com/q/ks?s=MA

  # Open URL
  #  myURL='http://ichart.finance.yahoo.com/table.csv?'+\
  #                       's=%s&d=10&e=20&f=2010&g=d&a=9&b=20&c=2010'%t +\
  #                       '&ignore=.csv'

  myURL='http://finance.yahoo.com/q/ks?s=%s'%ticker

  if (DEBUG ):
      print myURL

  
    
  c=urllib2.urlopen(myURL)

  soup=BeautifulSoup(c.read())
  if DEBUG:
    print soup

  keyCount=0
  #StringToFind="EPS"
  key=""
  value=""
  keys={}
  keyStats={}
  foundName=False;
  if DEBUG:
    logging.error('In getKeyStats');
    
  for td in soup('td'):
    # If Ticker Name was found, then price comes next.
    #if ( foundName ):
    #  logging.error('Looking for Price %s', td.text);
    #  key='Price';
    #  keys[keyCount]=key;
    #  keyCount=keyCount + 1;
    #  price=getPrice( td.text ) ;
    #  logging.debug('price is %s', price);
    #  keyStats[key]=price ;
    #  foundName=False;
    #  continue;

    # Looking for the Ticker Name - For INTC it will be INTEL
    #if ('class' in dict(td.attrs) and td['class']=='ygtb'):
    #if ('class' in dict(td.attrs) and td['class']=='title'):
    #  logging.error('Looking for Ticker Name %s', td.text);
    #  key='Ticker Name';
    #  keys[keyCount]=key
    #  keyCount=keyCount + 1
    #  keyStats[key]=td.text
    #  foundName=True;
    #  continue;

                    
    # Prints the heading
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tablehead1'):
      key=td.text
      keys[keyCount]=key
      keyCount=keyCount + 1
      if DEBUG:
        logging.debug('getKeyStats: key= %s, keycount=%d ', key, keyCount);
      if DEBUG:
        print "*** getKeyStats: Key is ***"
        print key
        
      continue
  # Prints the Value
    if ('class' in dict(td.attrs) and td['class']=='yfnc_tabledata1'):
        value=td.text
        
        if DEBUG:
          print "*** value = ***"
          print value
          
        keyStats[key]=value
        continue



 # Look for Price
  for td in soup('span'):
    # If Ticker Name was found, then price comes next.
    #if ( foundName ):
    if ('class' in dict(td.attrs) and td['class']=='time_rtq_ticker'):
      if DEBUG:
        logging.error('Looking for Price %s', td.text);
      key='Price';
      keys[keyCount]=key;
      keyCount=keyCount + 1;
      price=td.text  ;
      logging.debug('price is %s', price);
      keyStats[key]=price ;
      foundName=False;
      continue;
    
  for td in soup('div'):
    # Looking for the Ticker Name - For INTC it will be INTEL
    #if ('class' in dict(td.attrs) and td['class']=='ygtb'):
    if ('class' in dict(td.attrs) and td['class']=='title'):
      if DEBUG:
        logging.error('Looking for Ticker Name %s', td.text);
      key='Ticker Name';
      keys[keyCount]=key
      keyCount=keyCount + 1
      keyStats[key]=td.text
      foundName=True;
      continue;                   
   
# End Look for Price

# Look for Title
  allDivs=soup.findAll("div", { "class" : "title" });
  for div in allDivs:
    value = div.find('h2');
    key="title";
    keys[keyCount]=key;
    keyCount=keyCount + 1
    keyStats[key]=value.text
    
  #for k in keyStats:
  #   print keyStats[k]

  #print keyStats["Diluted EPS (ttm):"]
  if DEBUG:
    print keyCount

  return keyStats, keyCount, keys


def getValueFromKey( keyStats, key ):
  returnValue=keyStats[key]
  # Strip out the %
  returnValue=returnValue.replace('%','')
  # Strip out the Commas
  returnValue=returnValue.replace(',','')
  
  if (( returnValue=="NA" ) or  ( returnValue=="N/A" ) ):
    returnValue="0.0"
    
  return returnValue








  