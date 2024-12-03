import { useState } from 'react'
import './App.css'
import { TextField, Button, Container, Typography, Box, CircularProgress, Card, CardContent, Chip, Grid, Accordion, AccordionSummary, AccordionDetails } from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'

function App() {
  const [keywords, setKeywords] = useState('')
  const [loading, setLoading] = useState(false)
  const [jobs, setJobs] = useState([])
  const [companiesByKeyword, setCompaniesByKeyword] = useState({})

  const handleSearch = async () => {
    setLoading(true)
    setJobs([])
    setCompaniesByKeyword({})
    
    try {
      const keywordList = keywords.split(',').map(k => k.trim()).filter(k => k)
      console.log('Searching for keywords:', keywordList)
      
      const response = await fetch('http://localhost:8000/scrape-jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keywords: keywordList,
          max_jobs_per_keyword: 10
        }),
      })
      
      const data = await response.json()
      console.log('Response:', data)
      
      if (response.ok) {
        if (data.jobs && data.jobs.length > 0) {
          setJobs(data.jobs)
          setCompaniesByKeyword(data.companies_by_keyword || {})
          console.log('Jobs found:', data.jobs.length)
        } else {
          alert('No jobs found for the given keywords. Try different keywords.')
        }
      } else {
        console.error('Server error:', data)
        alert(`Error: ${data.detail || 'Failed to fetch jobs. Please try again.'}`)
      }
    } catch (error) {
      console.error('Network error:', error)
      alert('Network error: Could not connect to the server. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Wellfound Job Scraper
      </Typography>
      
      <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          label="Enter keywords (comma-separated)"
          value={keywords}
          onChange={(e) => setKeywords(e.target.value)}
          placeholder="e.g., python developer, react developer"
          disabled={loading}
        />
        <Button
          variant="contained"
          onClick={handleSearch}
          disabled={loading || !keywords.trim()}
          sx={{ minWidth: 120 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Search'}
        </Button>
      </Box>

      {companiesByKeyword && Object.keys(companiesByKeyword).length > 0 && (
        <Accordion sx={{ mb: 2 }}>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Typography variant="h6">Companies Hiring by Keyword</Typography>
          </AccordionSummary>
          <AccordionDetails>
            {Object.entries(companiesByKeyword).map(([keyword, companies]) => (
              <Box key={keyword} sx={{ mb: 2 }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  {keyword}:
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {companies.map((company) => (
                    <Chip key={company} label={company} />
                  ))}
                </Box>
              </Box>
            ))}
          </AccordionDetails>
        </Accordion>
      )}

      <Grid container spacing={2}>
        {jobs.map((job, index) => (
          <Grid item xs={12} md={6} lg={4} key={index}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" component="div" gutterBottom>
                  {job.title}
                </Typography>
                <Typography color="text.secondary" gutterBottom>
                  {job.company}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  📍 {job.location}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  🔍 Keyword: {job.keyword}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  {job.job_link && (
                    <Button 
                      variant="outlined" 
                      href={job.job_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      size="small"
                      sx={{ mr: 1, mb: 1 }}
                    >
                      View Job
                    </Button>
                  )}
                  {job.company_link && (
                    <Button
                      variant="outlined"
                      href={job.company_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      size="small"
                      sx={{ mb: 1 }}
                    >
                      View Company
                    </Button>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}

export default App