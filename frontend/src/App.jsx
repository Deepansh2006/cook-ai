import { useEffect, useMemo, useState } from 'react';
import { Container, CssBaseline, Paper, Tab, Tabs, Typography, Box, AppBar } from '@mui/material';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import RecommendForm from './components/RecommendForm';
import HistoryList from './components/HistoryList';
import { loadToken, saveToken, clearToken } from './services/api';

const tabLabels = ['Login', 'Register', 'Recommend', 'History'];

function App() {
  const [activeTab, setActiveTab] = useState(0);
  const [token, setToken] = useState('');
  const [alertMessage, setAlertMessage] = useState('');
  const [alertSeverity, setAlertSeverity] = useState('success');
  const [historyRefresh, setHistoryRefresh] = useState(0);

  useEffect(() => {
    const saved = loadToken();
    if (saved) {
      setToken(saved);
      setActiveTab(2);
    }
  }, []);

  const loggedIn = useMemo(() => Boolean(token), [token]);

  const handleLogin = (newToken) => {
    setToken(newToken);
    saveToken(newToken);
    setAlertMessage('Logged in successfully.');
    setAlertSeverity('success');
    setActiveTab(2);
  };

  const handleLogout = () => {
    setToken('');
    clearToken();
    setAlertMessage('Logged out successfully.');
    setAlertSeverity('info');
    setActiveTab(0);
  };

  const handleShowAlert = (message, severity = 'error') => {
    setAlertMessage(message);
    setAlertSeverity(severity);
  };

  return (
    <>
      <CssBaseline />
      <AppBar position="static" color="primary">
        <Container maxWidth="md">
          <Box py={2} display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h5" color="white">
              Cook AI
            </Typography>
            <Box>
              {loggedIn && (
                <Typography variant="body2" color="white">
                  Token active
                </Typography>
              )}
            </Box>
          </Box>
        </Container>
      </AppBar>
      <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
        <Paper elevation={4} sx={{ p: 3 }}>
          <Tabs
            value={activeTab}
            onChange={(event, value) => setActiveTab(value)}
            textColor="primary"
            indicatorColor="primary"
            variant="fullWidth"
            sx={{ mb: 3 }}
          >
            {tabLabels.map((label, index) => (
              <Tab
                key={label}
                label={label}
                disabled={index >= 2 && !loggedIn && index !== 2 ? false : false}
              />
            ))}
          </Tabs>

          {alertMessage && (
            <Box sx={{ mb: 2 }}>
              <Paper sx={{ p: 2, backgroundColor: alertSeverity === 'error' ? '#fdecea' : '#e8f5e9' }}>
                <Typography color={alertSeverity === 'error' ? 'error' : 'success.main'}>
                  {alertMessage}
                </Typography>
              </Paper>
            </Box>
          )}

          {activeTab === 0 && <LoginForm onLogin={handleLogin} onError={handleShowAlert} loggedIn={loggedIn} />}
          {activeTab === 1 && <RegisterForm onRegister={handleLogin} onError={handleShowAlert} />}
          {activeTab === 2 && (
            <RecommendForm
              token={token}
              onError={handleShowAlert}
              onSuccess={(message) => handleShowAlert(message, 'success')}
            />
          )}
          {activeTab === 3 && (
            <HistoryList
              token={token}
              refreshKey={historyRefresh}
              onError={handleShowAlert}
              onLogout={handleLogout}
            />
          )}
        </Paper>
      </Container>
    </>
  );
}

export default App;
