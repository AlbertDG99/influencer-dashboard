'use client';


import { 
    Container, 
    Typography, 
    Box,
    Alert
} from '@mui/material';
import SeleniumScraper from './SeleniumScraper';

export default function InfluencerDashboard() {
    return (
        <Container maxWidth="lg" sx={{ py: 4 }}>
            <Box sx={{ textAlign: 'center', mb: 4 }}>
                <Typography variant="h3" component="h1" gutterBottom>
                    📸 Instagram Selenium Scraper
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
                    Scraping manual con Selenium para superar las limitaciones de Instagram
                </Typography>
                <Alert severity="info" sx={{ mb: 3 }}>
                    <strong>🔥 Scraping Avanzado:</strong> Usa Selenium para simular un navegador real y obtener TODOS los posts de un perfil, 
                    superando las limitaciones de 12 posts de los métodos tradicionales.
                </Alert>
            </Box>

            <SeleniumScraper />
        </Container>
    );
} 