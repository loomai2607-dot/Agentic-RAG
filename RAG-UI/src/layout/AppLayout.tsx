// layout/AppLayout.tsx
import { Box, Drawer, List, ListItem, ListItemText, AppBar, Toolbar, Typography } from '@mui/material';
import { Link, Outlet } from 'react-router-dom';

const drawerWidth = 240;



export default function AppLayout() {
  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed" sx={{ zIndex: 1201 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            AI App Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <List>
  <ListItem button component={Link} to="/">
    <ListItemText primary="Home" />
  </ListItem>

  <ListItem button component={Link} to="/rag">
    <ListItemText primary="RAG UI" />
  </ListItem>

  <ListItem
    button
    component="a"
    href={import.meta.env.VITE_CALL_SUMMARY_URL}
    target="_blank"
    rel="noopener noreferrer"
  >
    <ListItemText primary="Call Summarization" />
  </ListItem>
</List>

      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, p: 3, ml: `${drawerWidth}px` }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
}