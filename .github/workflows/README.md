# Deployment Process: S3 Block & Agent Configuration
Welcome to the deployment guide for managing your S3 blocks and Prefect agent configurations. This document will walk you through the essential steps for both the initial setup and regular deployment process.

## Initial Setup
During the initial deployment, you'll need to create an S3 block, with a default name set to "prod". If you'd like to change this name, follow these instructions carefully.

1. Create an S3 Block
Default S3 Block Name: prod
Input Parameter: s3_block_name
Important: If you decide to change the S3 block name, make sure you update the S3_BLOCK_NAME in the main.yaml file. Failing to synchronize these names will lead to deployment errors.

2. Configure the Work Queue
Default Work Queue: dataflowops
Variable: PROJECT
Note: The default work queue is set to dataflowops. If you're using a different queue, update the PROJECT variable in the main.yaml file to reflect this change.

## Regular Deployment Process
Once your initial setup is complete, follow these guidelines for subsequent deployments:

3. Prefect Version Synchronization
Variable: PREFECT_VERSION
The PREFECT_VERSION defined during the initial agent deployment can differ from the version specified in main.yaml. However, if you encounter issues due to a version mismatch between your agent and workflow, consider synchronizing the versions to avoid conflicts. In such cases, re-trigger the deployment process by executing the ecs_prefect_agent.yml workflow.

## Troubleshooting
S3 Block Name Mismatch: Ensure that the name is consistently updated across your setup and deployment scripts.
Work Queue Changes: Always verify that any change in the work queue is mirrored in the PROJECT variable within main.yaml.
Prefect Version Conflicts: If deployment issues arise, version synchronization between the agent and workflow may be necessary.

## Conclusion
By following this guide, you can ensure smooth deployment of your Prefect agents and S3 blocks. Stay vigilant when modifying any configurations and ensure consistency across all files to avoid potential errors.

