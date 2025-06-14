'use client';

import { useEffect, useState } from 'react';
import { Alert, CircularProgress } from '@mui/material';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export default function BackendStatus() {
    const [status, setStatus] = useState<'loading' | 'ok' | 'error'>('loading');

    useEffect(() => {
        async function checkBackend() {
            try {
                const res = await fetch(`${API_BASE_URL}/ping`);
                if (res.ok) {
                    setStatus('ok');
                } else {
                    setStatus('error');
                }
            } catch (err) {
                setStatus('error');
            }
        }
        checkBackend();
    }, []);

    if (status === 'loading') {
        return <CircularProgress size={24} />;
    }

    if (status === 'ok') {
        return <Alert severity="success" sx={{ mb: 2 }}>Backend detected</Alert>;
    }

    return <Alert severity="error" sx={{ mb: 2 }}>Cannot reach backend</Alert>;
}
