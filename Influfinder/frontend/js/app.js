(() => {
	const state = { page: 1, pageSize: 12, lastEndpoint: "/api/influencers" };

	const els = {
		q: document.querySelector('#q'),
		category: document.querySelector('#category'),
		list: document.querySelector('#list'),
		placeholder: document.querySelector('#placeholder'),
		pageInfo: document.querySelector('#pageInfo'),
		pager: document.querySelector('#pager'),
		searchBtn: document.querySelector('#searchBtn'),
		trendingBtn: document.querySelector('#trendingBtn'),
		prevPage: document.querySelector('#prevPage'),
		nextPage: document.querySelector('#nextPage'),
		exportCsvBtn: document.querySelector('#exportCsvBtn'),
		exportXlsxBtn: document.querySelector('#exportXlsxBtn'),
		themeToggle: document.querySelector('#themeToggle'),
		settingsBtn: document.querySelector('#settingsBtn'),
		settingsModal: document.querySelector('#settingsModal'),
		closeModal: document.querySelector('#closeModal'),
		accessToken: document.querySelector('#accessToken'),
		businessAccountId: document.querySelector('#businessAccountId'),
		apiVersion: document.querySelector('#apiVersion'),
		saveSettings: document.querySelector('#saveSettings'),
		clearCache: document.querySelector('#clearCache'),
	};

	// Load saved credentials
	function loadCredentials() {
		els.accessToken.value = localStorage.getItem('instagram_access_token') || '';
		els.businessAccountId.value = localStorage.getItem('instagram_business_account_id') || '';
		els.apiVersion.value = localStorage.getItem('instagram_api_version') || 'v19.0';
	}

	// Save credentials
	function saveCredentials() {
		localStorage.setItem('instagram_access_token', els.accessToken.value);
		localStorage.setItem('instagram_business_account_id', els.businessAccountId.value);
		localStorage.setItem('instagram_api_version', els.apiVersion.value);
		els.settingsModal.style.display = 'none';
	}

	// Clear cache
	function clearCache() {
		localStorage.removeItem('instagram_access_token');
		localStorage.removeItem('instagram_business_account_id');
		localStorage.removeItem('instagram_api_version');
		els.accessToken.value = '';
		els.businessAccountId.value = '';
		els.apiVersion.value = 'v19.0';
	}

	// Modal controls
	els.settingsBtn.addEventListener('click', () => {
		els.settingsModal.style.display = 'block';
		loadCredentials();
	});

	els.closeModal.addEventListener('click', () => {
		els.settingsModal.style.display = 'none';
	});

	els.saveSettings.addEventListener('click', saveCredentials);
	els.clearCache.addEventListener('click', clearCache);

	// Close modal when clicking outside
	window.addEventListener('click', (e) => {
		if (e.target === els.settingsModal) {
			els.settingsModal.style.display = 'none';
		}
	});

	function qs(params) {
		const usp = new URLSearchParams(params);
		return `?${usp.toString()}`;
	}

	async function fetchList(endpoint) {
		const url = `${endpoint}${qs({ q: els.q.value || '', category: els.category.value || '', page: state.page, page_size: state.pageSize })}`;
		const res = await fetch(url);
		if (!res.ok) throw new Error('Error de API');
		return res.json();
	}

	function render(items) {
		if (!items || items.length === 0) {
			els.placeholder.style.display = 'block';
			els.list.style.display = 'none';
			els.pager.style.display = 'none';
			return;
		}

		els.placeholder.style.display = 'none';
		els.list.style.display = 'grid';
		els.pager.style.display = 'flex';

		els.list.innerHTML = items.map(item => {
			return `
				<li class="card">
					<img src="${item.avatar_url || 'https://i.pravatar.cc/150'}" alt="${item.username}" />
					<div>
						<h3>@${item.username} · ${item.full_name}</h3>
						<p>${item.bio || ''}</p>
						<p class="pill">${item.followers.toLocaleString()} seguidores · ${Math.round(item.engagement_rate*1000)/10}% ER</p>
					</div>
				</li>
			`;
		}).join('');
	}

	async function load(endpoint) {
		try {
			const data = await fetchList(endpoint);
			render(data.items || []);
			els.pageInfo.textContent = `Página ${data.page} de ${data.total_pages} · ${data.total} resultados`;
			state.lastEndpoint = endpoint;
		} catch (e) {
			console.error(e);
			els.placeholder.style.display = 'block';
			els.list.style.display = 'none';
			els.pager.style.display = 'none';
			els.placeholder.innerHTML = '<p>Error cargando datos</p>';
		}
	}

	els.searchBtn.addEventListener('click', () => { state.page = 1; load('/api/influencers'); });
	els.trendingBtn.addEventListener('click', () => { state.page = 1; load('/api/influencers/trending'); });
	els.prevPage.addEventListener('click', () => { if (state.page > 1) { state.page--; load(state.lastEndpoint); } });
	els.nextPage.addEventListener('click', () => { state.page++; load(state.lastEndpoint); });

	function openFile(endpoint) {
		const url = `${endpoint}${qs({ q: els.q.value || '', category: els.category.value || '', page: state.page, page_size: state.pageSize })}`;
		window.open(url, '_blank');
	}
	els.exportCsvBtn.addEventListener('click', () => openFile('/api/export/csv'));
	els.exportXlsxBtn.addEventListener('click', () => openFile('/api/export/xlsx'));

	// theme
	const prefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
	function setTheme(light) {
		if (light) document.documentElement.classList.add('light');
		else document.documentElement.classList.remove('light');
		localStorage.setItem('theme', light ? 'light' : 'dark');
	}
	els.themeToggle.addEventListener('click', () => setTheme(!document.documentElement.classList.contains('light')));
	setTheme(localStorage.getItem('theme') ? localStorage.getItem('theme') === 'light' : prefersLight);

	// Load credentials on startup
	loadCredentials();
})();
