import {
  Cloud,
  LayoutDashboard,
  Server,
  Database,
  ShieldCheck,
  HeartPulse,
  MessageSquare,
} from "lucide-react";

import "./App.css";

function App() {
  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Cloud size={28} />
          <span>AWS Assistant</span>
        </div>

        <nav className="nav-menu">
          <button className="nav-item active">
            <LayoutDashboard size={20} />
            Dashboard
          </button>

          <button className="nav-item">
            <Server size={20} />
            Resources
          </button>

          <button className="nav-item">
            <ShieldCheck size={20} />
            Security
          </button>

          <button className="nav-item">
            <HeartPulse size={20} />
            Health
          </button>

          <button className="nav-item">
            <MessageSquare size={20} />
            AI Assistant
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <div>
            <p className="eyebrow">CLOUD OVERVIEW</p>
            <h1>AWS Environment</h1>
            <p className="subtitle">
              Monitor resources, security, and environment health.
            </p>
          </div>

          <div className="connection-status">
            <span className="status-dot"></span>
            AWS Connected
          </div>
        </header>

        {/* Resource Cards */}
        <section className="cards">
          <div className="card">
            <Server size={24} />
            <p>EC2 Instances</p>
            <h2>0</h2>
            <span>No instances running</span>
          </div>

          <div className="card">
            <Database size={24} />
            <p>S3 Buckets</p>
            <h2>1</h2>
            <span>blue-image-app</span>
          </div>

          <div className="card">
            <ShieldCheck size={24} />
            <p>IAM Users</p>
            <h2>2</h2>
            <span>Users detected</span>
          </div>

          <div className="card">
            <HeartPulse size={24} />
            <p>CloudWatch Alarms</p>
            <h2>0</h2>
            <span>No alarms found</span>
          </div>
        </section>

        {/* Security */}
        <section className="section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">SECURITY</p>
              <h2>Security Findings</h2>
            </div>
            <span className="finding-count">3 findings</span>
          </div>

          <div className="findings">
            <div className="finding critical">
              <span className="finding-icon">!</span>
              <div>
                <h3>Public S3 Access</h3>
                <p>
                  The bucket policy allows public read access to objects.
                </p>
              </div>
              <span className="severity">Critical</span>
            </div>

            <div className="finding warning">
              <span className="finding-icon">!</span>
              <div>
                <h3>Broad S3 Permissions</h3>
                <p>
                  image_upload_user has AmazonS3FullAccess permissions.
                </p>
              </div>
              <span className="severity">Review</span>
            </div>

            <div className="finding medium">
              <span className="finding-icon">!</span>
              <div>
                <h3>S3 Versioning Disabled</h3>
                <p>
                  Object versioning is not currently enabled for the bucket.
                </p>
              </div>
              <span className="severity">Medium</span>
            </div>
          </div>
        </section>

        {/* AI Input */}
        <section className="assistant-box">
          <div className="assistant-title">
            <MessageSquare size={20} />
            <span>Ask the AWS Cloud Assistant</span>
          </div>

          <div className="question-box">
            <input
              type="text"
              placeholder="Ask about your AWS environment..."
            />
            <button>Ask</button>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;