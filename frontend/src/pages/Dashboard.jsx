import {
  Server,
  Database,
  ShieldCheck,
  HeartPulse,
  AlertTriangle,
} from "lucide-react";

function Dashboard() {
  return (
    <>
      {/* Header */}
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

      {/* Security Findings */}
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
            <AlertTriangle size={22} />
            <div>
              <h3>Public S3 Access</h3>
              <p>
                The bucket policy allows public read access to objects.
              </p>
            </div>
            <span className="severity">Critical</span>
          </div>

          <div className="finding warning">
            <AlertTriangle size={22} />
            <div>
              <h3>Broad S3 Permissions</h3>
              <p>
                image_upload_user has AmazonS3FullAccess permissions.
              </p>
            </div>
            <span className="severity">Review</span>
          </div>

          <div className="finding medium">
            <AlertTriangle size={22} />
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
    </>
  );
}

export default Dashboard;