'use client';

import { useState } from 'react';
import { Button, TextField, CircularProgress, Alert, Card, CardContent, Typography, Grid, Box } from '@mui/material';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface InstagramProfile {
    username: string;
    full_name: string;
    biography: string;
    followers_count: number;
    following_count: number;
    profile_pic_url: string;
    latest_post_url: string | null;
}

export default function InfluencerDashboard() {
    const [username, setUsername] = useState('');
    const [profile, setProfile] = useState<InstagramProfile | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!username) return;

        setIsLoading(true);
        setError(null);
        setProfile(null);

        try {
            const res = await fetch(`${API_BASE_URL}/instagram-profile/${username}`);

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || 'Failed to fetch profile.');
            }

            const data: InstagramProfile = await res.json();
            setProfile(data);

        } catch (err: any) {
            console.error("--- Frontend Error Detallado ---", err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-4xl">
            <form onSubmit={handleSearch} className="flex gap-4 mb-8">
                <TextField
                    label="Instagram Username"
                    variant="outlined"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={isLoading}
                    fullWidth
                />
                <Button type="submit" variant="contained" disabled={isLoading || !username} sx={{ minWidth: 120 }}>
                    {isLoading ? <CircularProgress size={24} /> : 'Search'}
                </Button>
            </form>

            {error && <Alert severity="error" className="mb-4">{error}</Alert>}

            {profile && (
                <Card>
                    <CardContent>
                        <Grid container spacing={4}>
                            <Grid item xs={12} md={4}>
                                <img
                                    src={profile.profile_pic_url}
                                    alt={`Profile picture of ${profile.full_name}`}
                                    style={{ width: '100%', borderRadius: '50%' }}
                                />
                            </Grid>
                            <Grid item xs={12} md={8}>
                                <Typography variant="h4" component="h2" gutterBottom>
                                    {profile.full_name}
                                </Typography>
                                <Typography variant="h6" color="text.secondary" gutterBottom>
                                    @{profile.username}
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 3, my: 2 }}>
                                    <Typography>
                                        <b>{profile.followers_count.toLocaleString()}</b> Followers
                                    </Typography>
                                    <Typography>
                                        <b>{profile.following_count.toLocaleString()}</b> Following
                                    </Typography>
                                </Box>
                                <Typography variant="body1" paragraph>
                                    {profile.biography}
                                </Typography>
                            </Grid>
                            {profile.latest_post_url && (
                                <Grid item xs={12}>
                                    <Typography variant="h5" component="h3" gutterBottom>
                                        Latest Post
                                    </Typography>
                                    <img
                                        src={profile.latest_post_url}
                                        alt={`Latest post from ${profile.username}`}
                                        style={{ width: '100%', maxWidth: '400px', borderRadius: '8px' }}
                                    />
                                </Grid>
                            )}
                        </Grid>
                    </CardContent>
                </Card>
            )}
        </div>
    );
} 