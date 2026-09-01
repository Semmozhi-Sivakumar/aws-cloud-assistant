import {
  Server,
  Database,
  Users,
  HardDrive,
  Lock,
  Layers,
} from "lucide-react";

function Resources() {
  return (
    <>
      {/* Header */}
      <header className="header">
        <div>
          <p className="eyebrow">AWS RESOURCES</p>
          <h1>Resources</h1>
          <p className="subtitle">
            View the resources detected in your AWS environment.
          </p>
        </div>
      </header>

      {/* EC2 Section */}
      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">COMPUTE</p>
            <h2>EC2 Instances</h2>
          </div>

          <span className="finding-count">0 instances</span>
        </div>

        <div className="empty-state">
          <Server size={40} />
          <h3>No EC2 Instances Found</h3>
          <p>
            No EC2 instances are currently running in the monitored AWS environment.
          </p>
        </div>
      </section>

      {/* S3 Section */}
      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">STORAGE</p>
            <h2>S3 Buckets</h2>
          </div>

          <span className="finding-count">1 bucket</span>
        </div>

        <div className="resource-grid">
          <div className="resource-card">
            <div className="resource-icon">
              <Database size={24} />
            </div>

            <div className="resource-info">
              <h3>blue-image-app</h3>
              <p>AWS S3 Bucket</p>
            </div>

            <div className="resource-details">
              <div>
                <HardDrive size={16} />
                <span>3 Objects</span>
              </div>

              <div>
                <Layers size={16} />
                <span>2.4 MB Used</span>
              </div>

              <div>
                <Lock size={16} />
                <span>AES256 Encryption</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* IAM Section */}
      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">IDENTITY & ACCESS</p>
            <h2>IAM Users</h2>
          </div>

          <span className="finding-count">2 users</span>
        </div>

        <div className="resource-grid">
          <div className="iam-user-card">
            <Users size={24} />

            <div>
              <h3>cloud-assistant</h3>
              <p>Read-only AWS access policies detected</p>
            </div>
          </div>

          <div className="iam-user-card">
            <Users size={24} />

            <div>
              <h3>image_upload_user</h3>
              <p>AmazonS3FullAccess policy detected</p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Resources;