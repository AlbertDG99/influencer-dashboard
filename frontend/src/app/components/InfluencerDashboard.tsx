'use client';

import { useState } from 'react';
import { Button, TextField, CircularProgress, Alert, Card, CardContent, Typography, Grid, Box, Divider } from '@mui/material';
import Image from 'next/image';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

interface InstagramProfile {
    username: string;
    full_name: string;
    biography: string;
    followers_count: number;
    following_count: number;
    profile_pic_url: string;
    latest_post_url: string | null;
}

function InfluencerCard({ profile }: { profile: InstagramProfile }) {
    return (
        <Card sx={{ height: '100%' }}>
            <CardContent>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={4}>
                        <Image
                            src={profile.profile_pic_url}
                            alt={`Profile picture of ${profile.full_name}`}
                            width={80}
                            height={80}
                            style={{ borderRadius: '50%' }}
                        />
                    </Grid>
                    <Grid item xs={8}>
                        <Typography variant="h6" component="h3" noWrap>
                            {profile.full_name || profile.username}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            @{profile.username}
                        </Typography>
                    </Grid>
                </Grid>
                <Box sx={{ display: 'flex', gap: 2, my: 1, justifyContent: 'center' }}>
                    <Typography variant="body2">
                        <b>{profile.followers_count.toLocaleString()}</b> Followers
                    </Typography>
                    <Typography variant="body2">
                        <b>{profile.following_count.toLocaleString()}</b> Following
                    </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{
                    height: 60,
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                }}>
                    {profile.biography}
                </Typography>
            </CardContent>
        </Card>
    );
}

export default function InfluencerDashboard() {
    // State for single profile search
    const [username, setUsername] = useState('');
    const [profile, setProfile] = useState<InstagramProfile | null>(null);
    const [isProfileLoading, setIsProfileLoading] = useState(false);
    const [profileError, setProfileError] = useState<string | null>(null);

    // State for hashtag discovery
    const [hashtag, setHashtag] = useState('');
    const [discoveredProfiles, setDiscoveredProfiles] = useState<InstagramProfile[]>([]);
    const [isDiscovering, setIsDiscovering] = useState(false);
    const [discoverError, setDiscoverError] = useState<string | null>(null);


    const handleProfileSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!username) return;

        setIsProfileLoading(true);
        setProfileError(null);
        setProfile(null);

        try {
            const res = await fetch(
                `${API_BASE_URL}/instagram/profile/${encodeURIComponent(username)}`
            );

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || 'Failed to fetch profile.');
            }

            const data: InstagramProfile = await res.json();
            setProfile(data);

        } catch (err: unknown) {
            console.error("--- Frontend Error Detallado ---", err);
            if (err instanceof Error) {
                setProfileError(err.message);
            } else {
                setProfileError('Unknown error');
            }
        } finally {
            setIsProfileLoading(false);
        }
    };
    
    const handleDiscoverSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!hashtag) return;

        setIsDiscovering(true);
        setDiscoverError(null);
        setDiscoveredProfiles([]);

        try {
            const res = await fetch(
                `${API_BASE_URL}/instagram/discover/${encodeURIComponent(hashtag)}`
            );

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || 'Failed to discover influencers.');
            }

            const data: InstagramProfile[] = await res.json();
            setDiscoveredProfiles(data);

        } catch (err: unknown) {
            console.error("--- Frontend Error Detallado ---", err);
            if (err instanceof Error) {
                setDiscoverError(err.message);
            } else {
                setDiscoverError('Unknown error');
            }
        } finally {
            setIsDiscovering(false);
        }
    };


    return (
        <div className="w-full max-w-6xl">
            {/* --- Single Profile Search --- */}
            <Typography variant="h4" gutterBottom>Search Profile</Typography>
            <form onSubmit={handleProfileSearch} className="flex gap-4 mb-8">
                <TextField
                    label="Instagram Username"
                    variant="outlined"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={isProfileLoading}
                    fullWidth
                />
                <Button type="submit" variant="contained" disabled={isProfileLoading || !username} sx={{ minWidth: 120 }}>
                    {isProfileLoading ? <CircularProgress size={24} /> : 'Search'}
                </Button>
            </form>

            {profileError && <Alert severity="error" className="mb-4">{profileError}</Alert>}

            {profile && (
                <Card className="mb-8">
                    <CardContent>
                        <Grid container spacing={4}>
                            <Grid item xs={12} md={3}>
                                <Image
                                    src={profile.profile_pic_url}
                                    alt={`Profile picture of ${profile.full_name}`}
                                    width={200}
                                    height={200}
                                    style={{ width: '100%', borderRadius: '50%' }}
                                />
                            </Grid>
                            <Grid item xs={12} md={9}>
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
                        </Grid>
                    </CardContent>
                </Card>
            )}

            <Divider sx={{ my: 6 }} />

            {/* --- Discover Influencers by Hashtag --- */}
            <Typography variant="h4" gutterBottom>Discover Influencers by Hashtag</Typography>
             <form onSubmit={handleDiscoverSearch} className="flex gap-4 mb-8">
                <TextField
                    label="Instagram Hashtag (e.g., 'fashion')"
                    variant="outlined"
                    value={hashtag}
                    onChange={(e) => setHashtag(e.target.value)}
                    disabled={isDiscovering}
                    fullWidth
                />
                <Button type="submit" variant="contained" disabled={isDiscovering || !hashtag} sx={{ minWidth: 120 }}>
                    {isDiscovering ? <CircularProgress size={24} /> : 'Discover'}
                </Button>
            </form>
            
            {isDiscovering && (
                <Box sx={{ textAlign: 'center', my: 4 }}>
                    <CircularProgress />
                    <Typography color="text.secondary" sx={{ mt: 2 }}>
                        Discovering influencers... This may take several minutes.
                    </Typography>
                </Box>
            )}

            {discoverError && <Alert severity="error" className="mb-4">{discoverError}</Alert>}
            
            <Grid container spacing={3}>
                {discoveredProfiles.map(p => (
                    <Grid item xs={12} sm={6} md={4} key={p.username}>
                        <InfluencerCard profile={p} />
                    </Grid>
                ))}
            </Grid>
        </div>
    );
} 