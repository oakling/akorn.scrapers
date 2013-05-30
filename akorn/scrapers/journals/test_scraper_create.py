#this module will create a scraper class for each scraper just to check that they run
import unittest
 
##all the following scrapers use utils
import scrape_pr, scrape_iop, scrape_acs, scrape_arxiv,scrape_oup,scrape_npg,scrape_wiley
import scrape_pnas,scrape_atmos,scrape_jhu, scrape_oup2
#,scrape_science

#class TestPnas(unittest.TestCase):
  #def test_pnas(self):
	##this fails as the xpath is incorrect - needs checking
    #article = scrape_pnas.scrape('http://www.pnas.org/content/110/20/E1837.short?rss=1&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+pnas%2FSMZM+%28Current+Issue%29&utm_content=FeedBurner')
    
    #self.assertIsNotNone(article)

#class TestPhysRev(unittest.TestCase):
  #def test_pra(self):
    #article = scrape_pr.scrape('http://pra.aps.org/abstract/PRA/v85/i1/e010102')
    
    #self.assertIsNotNone(article)
    
#class TestNature(unittest.TestCase):
  #def test_npg(self):
    #article = scrape_npg.scrape('http://www.nature.com/nature/journal/v497/n7448/full/nature12073.html')
    
    #self.assertIsNotNone(article)

#class TestPhysRev(unittest.TestCase):
  #def test_pra(self):
    #article = scrape_pr.scrape('http://pra.aps.org/abstract/PRA/v85/i1/e010102')

    #self.assertIsNotNone(article)

  #def test_prb(self):
    #article = scrape_pr.scrape('http://prb.aps.org/abstract/PRB/v85/i11/e115303')

    #self.assertIsNotNone(article)
    

#class TestIOP(unittest.TestCase):
  #def test_iop1(self):
    #article = scrape_iop.scrape('http://iopscience.iop.org/1748-0221/7/03/C03017')
 
    #self.assertIsNotNone(article)

#class TestWiley(unittest.TestCase):
  #def test_wiley(self):
    #article = scrape_wiley.scrape('http://onlinelibrary.wiley.com/doi/10.1002/hec.2834/abstract')
##the following url doesn't work as the xpath is wrong in scraper
##http://onlinelibrary.wiley.com/doi/10.1111/boc.201300003/abstract

    #self.assertIsNotNone(article)
    
       
##these three scrapers pnas, science, molpharm, would appear not to work
#class TestNAS(unittest.TestCase):
  #def test_pnas(self):
	  ##this doesn't work, xpath error
    #article = scrape_pnas.scrape('http://www.pnas.org/content/109/10/E588.abstract')
    
    #self.assertIsNotNone(article)


##class TestScience(unittest.TestCase):
  ##def test_science(self):
    ##article = scrape_science.scrape('http://www.sciencemag.org/content/335/6073/1184')

    ##self.assertIsNotNone(article)
#class TestJHU(unittest.TestCase):
	#def test_jhu(self):
		#article=scrape_jhu.scrape('http://muse.jhu.edu/journals/american_journal_of_mathematics/toc/ajm.134.6.html')
		#self.assertIsNotNone(article)
		
##class TestACS(unittest.TestCase):
  ##def test_molpharm(self):
    ##article = scrape_acs.scrape('http://pubs.acs.org/doi/abs/10.1021/mp200447r')
###this scraper doesn't run in the first place
    ##self.assertIsNotNone(article)


#class TestArxiv(unittest.TestCase):
  #def test_arxiv1(self):
    #article = scrape_arxiv.scrape('http://arxiv.org/abs/1203.1816')

    #self.assertIsNotNone(article)


#class TestOUP(unittest.TestCase):
  #def test_oup(self):
    #article = scrape_oup.scrape('http://iwc.oxfordjournals.org/content/25/3/199.short?rss=1')

    #self.assertIsNotNone(article)
    
class TestOUP2(unittest.TestCase):
  def test_oup2(self):
    article = scrape_oup2.scrape('http://iwc.oxfordjournals.org/content/25/3/199.short?rss=1','/home/jo/sites/akorn_test_instance/src/akorn.scrapers/akorn/scrapers/journals/Data/OUP.xml')

    self.assertIsNotNone(article)

class TestOUPCompare(unittest.TestCase):
  def test_oupcompare(self):
    articleOld = scrape_oup.scrape('http://iwc.oxfordjournals.org/content/25/3/199.short?rss=1')
    articleNew = scrape_oup2.scrape('http://iwc.oxfordjournals.org/content/25/3/199.short?rss=1','/home/jo/sites/akorn_test_instance/src/akorn.scrapers/akorn/scrapers/journals/Data/OUP.xml')
    self.maxDiff=None
    self.assertEqual(articleOld['scraper'], articleNew['scraper'])
    self.assertEqual(articleOld['source_urls'], articleNew['source_urls'])
    self.assertEqual(articleOld['publisher'], articleNew['publisher'])
    self.assertEqual(articleOld['title'], articleNew['title'])
    self.assertEqual(articleOld['author_names'], articleNew['author_names'])
    self.assertEqual(articleOld['ids'], articleNew['ids'])
    self.assertEqual(articleOld['date'], articleNew['date'])

    self.assertEqual(articleOld['journal'], articleNew['journal'])
    self.assertEqual(articleOld['citation'], articleNew['citation'])

#class TestAtmos(unittest.TestCase):
 ##xpath fails here
 ##tree.xpath("//span[@class='pb_citation_header']")[0].text_content()
  #def test_atmos(self):
    #article = scrape_atmos.scrape('http://www.atmos-chem-phys.net/13/15/2013/acp-13-15-2013.html')

    #self.assertIsNotNone(article)

if __name__ == '__main__':
    unittest.main()
