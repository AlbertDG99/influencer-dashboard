'use client';

import { useState, useEffect } from 'react';
import { 
    Box, Typography, TextField, Button, Alert, Card, CardContent, 
    Accordion, AccordionSummary, AccordionDetails, Chip, List, ListItem, 
    ListItemText, CircularProgress, LinearProgress, Paper, Divider
} from '@mui/material';
import { 
    ExpandMore as ExpandMoreIcon, 
    Security as SecurityIcon, 
    BugReport as BugReportIcon,
    CheckCircle as CheckCircleIcon,
    Error as ErrorIcon,
    Info as InfoIcon
} from '@mui/icons-material';

interface SeleniumProgress {
    type: 'start' | 'info' | 'success' | 'error' | 'profile' | 'posts' | 'statistics' | 'complete';
    message?: string;
    data?: unknown;
}

interface SeleniumResult {
    success: boolean;
    method: string;
    username: string;
    profile: {
        username: string;
        full_name: string;
        posts_count: number;
        followers_count: number;
        following_count: number;
        bio: string;
        is_private: boolean;
        is_verified: boolean;
    };
    posts: Array<{
        shortcode: string;
        url: string;
        type: string;
        post_url: string;
    }>;
    statistics: {
        total_posts_in_profile: number;
        posts_scraped: number;
        posts_loaded_by_scroll: number;
        scraping_effectiveness: string;
    };
    selenium_info: {
        browser_used: string;
        authentication_status: boolean;
        anti_detection_measures: string[];
    };
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

interface AuthStatus {
    status: string;
    message: string;
    user_id?: string;
    cookie_count?: number;
    auth_type?: string;
    benefits?: string[];
    limitations?: string[];
}

export default function SeleniumScraper() {
    const [username, setUsername] = useState('');
    const [cookies, setCookies] = useState('');
    const [authStatus, setAuthStatus] = useState<AuthStatus | null>(null);
    const [isSeleniumScraping, setIsSeleniumScraping] = useState(false);
    const [seleniumProgress, setSeleniumProgress] = useState<SeleniumProgress[]>([]);
    const [seleniumResult, setSeleniumResult] = useState<SeleniumResult | null>(null);
    const [seleniumError, setSeleniumError] = useState<string | null>(null);
    const [realTimeProgress, setRealTimeProgress] = useState(false);

    const checkAuthStatus = async () => {
        try {
            const res = await fetch(`${API_BASE_URL}/instagram/auth/status`);
            if (res.ok) {
                const data: AuthStatus = await res.json();
                setAuthStatus(data);
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
        }
    };

    const setupFullAuth = async () => {
        if (!cookies.trim()) {
            setSeleniumError('Please provide Instagram cookies');
            return;
        }

        try {
            const res = await fetch(`${API_BASE_URL}/instagram/auth/full`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cookies: cookies.trim() })
            });

            if (!res.ok) {
                const errorData = await res.json() as { detail?: string };
                throw Error(errorData.detail || 'Failed to setup authentication');
            }

            setSeleniumError(null);
            await checkAuthStatus();
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown authentication error';
            setSeleniumError(errorMessage);
        }
    };

    const handleSeleniumScraping = async () => {
        if (!username.trim()) {
            setSeleniumError('Please provide a username');
            return;
        }

        setIsSeleniumScraping(true);
        setSeleniumError(null);
        setSeleniumResult(null);
        setSeleniumProgress([]);

        try {
            if (realTimeProgress) {
                // Streaming version
                const cookiesParam = cookies.trim() ? `?cookies=${encodeURIComponent(cookies.trim())}` : '';
                const eventSource = new EventSource(`${API_BASE_URL}/instagram/scrape-selenium-stream/${encodeURIComponent(username)}${cookiesParam}`);
                
                eventSource.onmessage = (event) => {
                    try {
                        const data: SeleniumProgress = JSON.parse(event.data);
                        setSeleniumProgress(prev => [...prev, data]);
                        
                        if (data.type === 'complete' || data.type === 'error') {
                            eventSource.close();
                            setIsSeleniumScraping(false);
                        }
                    } catch (error) {
                        console.error('Error parsing SSE data:', error);
                    }
                };

                eventSource.onerror = () => {
                    eventSource.close();
                    setIsSeleniumScraping(false);
                    setSeleniumError('Connection error during streaming');
                };
            } else {
                // Direct API call
                const res = await fetch(`${API_BASE_URL}/instagram/scrape-selenium/${encodeURIComponent(username)}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ cookies: cookies.trim() || null })
                });

                if (!res.ok) {
                    const errorData = await res.json() as { detail?: string };
                    throw Error(errorData.detail || 'Selenium scraping failed');
                }

                const data: SeleniumResult = await res.json();
                setSeleniumResult(data);
                setIsSeleniumScraping(false);
            }

        } catch (error) {
            console.error('Selenium scraping error:', error);
            setIsSeleniumScraping(false);
            const errorMessage = error instanceof Error ? error.message : 'Unknown Selenium scraping error';
            setSeleniumError(errorMessage);
        }
    };

    useEffect(() => {
        checkAuthStatus();
    }, []);

    return (
        <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
            {/* Authentication Status */}
            <Card sx={{ mb: 4 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <SecurityIcon />
                        Authentication Status
                    </Typography>
                    
                    {authStatus ? (
                        <Box>
                            <Chip 
                                label={authStatus.status.replace('_', ' ').toUpperCase()}
                                color={authStatus.status === 'full_authenticated' ? 'success' : 
                                       authStatus.status === 'basic_authenticated' ? 'warning' : 'error'}
                                sx={{ mb: 2 }}
                            />
                            <Typography variant="body2" color="text.secondary">
                                {authStatus.message}
                            </Typography>
                            
                            {authStatus.benefits && (
                                <Box sx={{ mt: 2 }}>
                                    <Typography variant="subtitle2" gutterBottom>Benefits:</Typography>
                                    <List dense>
                                        {authStatus.benefits.map((benefit, index) => (
                                            <ListItem key={index} sx={{ py: 0 }}>
                                                <ListItemText primary={`• ${benefit}`} />
                                            </ListItem>
                                        ))}
                                    </List>
                                </Box>
                            )}
                        </Box>
                    ) : (
                        <CircularProgress size={24} />
                    )}
                </CardContent>
            </Card>

            {/* Instagram Authentication Setup */}
            <Accordion sx={{ mb: 4 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <BugReportIcon />
                        Instagram Authentication Setup
                    </Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography variant="body2" color="text.secondary" paragraph>
                        Para obtener el máximo rendimiento del scraping con Selenium, configura tus cookies de Instagram:
                    </Typography>
                    
                    <Typography variant="subtitle2" gutterBottom>
                        🍪 Cómo obtener las cookies:
                    </Typography>
                    <Typography variant="body2" component="div" sx={{ mb: 2 }}>
                        <strong>Método 1 - Developer Tools:</strong>
                        <ol>
                            <li>Abre Instagram en Chrome y inicia sesión</li>
                            <li>Presiona F12 → Application → Storage → Cookies → https://www.instagram.com</li>
                            <li>Copia todas las cookies en formato: name1=value1; name2=value2; ...</li>
                        </ol>
                        
                        <strong>Método 2 - Console:</strong>
                        <ol>
                            <li>En la consola de Instagram ejecuta: <code>document.cookie</code></li>
                            <li>Copia el resultado completo</li>
                        </ol>
                    </Typography>

                    <TextField
                        label="Instagram Cookies"
                        placeholder="csrftoken=...; sessionid=...; ds_user_id=...; ..."
                        multiline
                        rows={4}
                        fullWidth
                        value={cookies}
                        onChange={(e) => setCookies(e.target.value)}
                        sx={{ mb: 2 }}
                    />

                    <Button 
                        variant="contained" 
                        onClick={setupFullAuth}
                        disabled={!cookies.trim()}
                    >
                        Setup Authentication
                    </Button>
                </AccordionDetails>
            </Accordion>

            {/* Selenium Scraping Configuration */}
            <Card sx={{ mb: 4 }}>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        🔥 Selenium Manual Scraping Configuration
                    </Typography>
                    
                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                        <Box sx={{ flex: 1 }}>
                            <TextField
                                label="Instagram Username"
                                placeholder="albertodfg99"
                                fullWidth
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                disabled={isSeleniumScraping}
                            />
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Button
                                variant="outlined"
                                onClick={() => setRealTimeProgress(!realTimeProgress)}
                                disabled={isSeleniumScraping}
                            >
                                {realTimeProgress ? 'Disable' : 'Enable'} Real-time Progress
                            </Button>
                            <Chip 
                                label={realTimeProgress ? 'Streaming ON' : 'Direct Call'} 
                                color={realTimeProgress ? 'primary' : 'default'}
                                size="small"
                            />
                        </Box>
                    </Box>

                    <Box sx={{ mt: 3 }}>
                        <Button
                            variant="contained"
                            size="large"
                            onClick={handleSeleniumScraping}
                            disabled={isSeleniumScraping || !username.trim()}
                            startIcon={isSeleniumScraping ? <CircularProgress size={20} /> : <BugReportIcon />}
                        >
                            {isSeleniumScraping ? 'Scraping...' : '🔥 Start Selenium Scraping'}
                        </Button>
                    </Box>

                    {seleniumError && (
                        <Alert severity="error" sx={{ mt: 2 }}>
                            {seleniumError}
                        </Alert>
                    )}
                </CardContent>
            </Card>

            {/* Real-time Progress */}
            {realTimeProgress && seleniumProgress.length > 0 && (
                <Card sx={{ mb: 4 }}>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            📊 Real-time Progress
                        </Typography>
                        
                        <Paper sx={{ maxHeight: 300, overflow: 'auto', p: 2, bgcolor: 'grey.50' }}>
                            {seleniumProgress.map((progress, index) => (
                                <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                    {progress.type === 'start' && <InfoIcon color="info" fontSize="small" />}
                                    {progress.type === 'success' && <CheckCircleIcon color="success" fontSize="small" />}
                                    {progress.type === 'error' && <ErrorIcon color="error" fontSize="small" />}
                                    {progress.type === 'complete' && <CheckCircleIcon color="success" fontSize="small" />}
                                    {progress.type === 'info' && <InfoIcon color="info" fontSize="small" />}
                                    
                                    <Typography variant="body2" component="span">
                                        {progress.message}
                                    </Typography>
                                </Box>
                            ))}
                        </Paper>
                    </CardContent>
                </Card>
            )}

            {/* Selenium Results */}
            {seleniumResult && (
                <Card>
                    <CardContent>
                        <Typography variant="h6" gutterBottom>
                            🎉 Selenium Scraping Results
                        </Typography>

                        {/* Profile Information */}
                        <Box sx={{ mb: 3 }}>
                            <Typography variant="subtitle1" gutterBottom>
                                👤 Profile Information
                            </Typography>
                            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: 'repeat(2, 1fr)', sm: 'repeat(4, 1fr)' }, gap: 2 }}>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="h6">{seleniumResult.profile.posts_count}</Typography>
                                    <Typography variant="body2" color="text.secondary">Posts</Typography>
                                </Paper>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="h6">{seleniumResult.profile.followers_count}</Typography>
                                    <Typography variant="body2" color="text.secondary">Followers</Typography>
                                </Paper>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="h6">{seleniumResult.profile.following_count}</Typography>
                                    <Typography variant="body2" color="text.secondary">Following</Typography>
                                </Paper>
                                <Paper sx={{ p: 2, textAlign: 'center' }}>
                                    <Typography variant="h6">{seleniumResult.posts.length}</Typography>
                                    <Typography variant="body2" color="text.secondary">Scraped</Typography>
                                </Paper>
                            </Box>
                        </Box>

                        <Divider sx={{ my: 3 }} />

                        {/* Statistics */}
                        <Box sx={{ mb: 3 }}>
                            <Typography variant="subtitle1" gutterBottom>
                                📈 Scraping Statistics
                            </Typography>
                            <Typography variant="body2">
                                <strong>Effectiveness:</strong> {seleniumResult.statistics.scraping_effectiveness}
                            </Typography>
                            <Typography variant="body2">
                                <strong>Method:</strong> {seleniumResult.method}
                            </Typography>
                            <Typography variant="body2">
                                <strong>Browser:</strong> {seleniumResult.selenium_info.browser_used}
                            </Typography>
                            <Typography variant="body2">
                                <strong>Authenticated:</strong> {seleniumResult.selenium_info.authentication_status ? 'Yes' : 'No'}
                            </Typography>

                            {/* Progress Bar */}
                            <Box sx={{ mt: 2 }}>
                                <LinearProgress 
                                    variant="determinate" 
                                    value={(seleniumResult.posts.length / seleniumResult.profile.posts_count) * 100}
                                    sx={{ height: 8, borderRadius: 4 }}
                                />
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                                    {seleniumResult.posts.length} of {seleniumResult.profile.posts_count} posts scraped 
                                    ({Math.round((seleniumResult.posts.length / seleniumResult.profile.posts_count) * 100)}%)
                                </Typography>
                            </Box>
                        </Box>

                        <Divider sx={{ my: 3 }} />

                        {/* Posts Preview */}
                        <Box>
                            <Typography variant="subtitle1" gutterBottom>
                                📸 Posts Found ({seleniumResult.posts.length})
                            </Typography>
                            <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(2, 1fr)', md: 'repeat(3, 1fr)' }, gap: 2 }}>
                                {seleniumResult.posts.slice(0, 6).map((post, index) => (
                                    <Paper key={post.shortcode} sx={{ p: 2 }}>
                                        <Typography variant="body2" noWrap>
                                            <strong>#{index + 1}:</strong> {post.shortcode}
                                        </Typography>
                                        <Typography variant="caption" color="text.secondary">
                                            Type: {post.type}
                                        </Typography>
                                    </Paper>
                                ))}
                            </Box>
                            
                            {seleniumResult.posts.length > 6 && (
                                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                                    ... and {seleniumResult.posts.length - 6} more posts
                                </Typography>
                            )}
                        </Box>
                    </CardContent>
                </Card>
            )}
        </Box>
    );
} 