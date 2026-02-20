package go_unit_test_bootcamp

import "testing"

// Simple test - verify that a single repository is indexed correctly
func TestIndexGitHubRepositoriesByOrg_basic(t *testing.T) {
    repos := []*GitHubRepository{
        {
            Organization: "devcloudninjas",
            Repository: "devops-bootcamp",
            Url: "https://github.com/devcloudninjas/devops-bootcamp",
            License: "MIT",
        },
    }

    result := IndexGitHubRepositoriesByOrg(repos)

    if k := len(result); k != 1 {
        t.Errorf("expected result map to have one key, but it has %d keys", k)
    }

    if n := len(result["devcloudninjas"]); n != 1 {
        t.Errorf("expected devcloudninjas organization to have one repository, but it has %d", n)
    }
}

// More complicated test - verify that multiple repositories are indexed correctly
func TestIndexGitHubRepositoriesByOrg_multiple(t *testing.T) {
    repos := []*GitHubRepository{
        {
            Organization: "devcloudninjas",
            Repository: "devops-bootcamp",
            Url: "https://github.com/devcloudninjas/devops-bootcamp",
            License: "MIT",
        },
        {
            Organization: "kubernetes",
            Repository: "kubernetes",
            Url: "https://github.com/kubernetes/kubernetes",
            License: "Apache-2.0",
        },
        {
            Organization: "devcloudninjas",
            Repository: "lead-terraform",
            Url: "https://github.com/devcloudninjas/lead-terraform",
            License: "MIT",
        },
    }

    result := IndexGitHubRepositoriesByOrg(repos)

    if k := len(result); k != 2 {
        t.Errorf("expected result map to have two keys, but it has %d keys", k)
    }

    if n := len(result["devcloudninjas"]); n != 2 {
        t.Errorf("expected devcloudninjas organization to have two repositories, but it has %d", n)
    }

    if n := len(result["kubernetes"]); n != 1 {
        t.Errorf("expected kubernetes organization to have one repository, but it has %d", n)
    }
}

// Edge case test - verify that zero input repositories results in an empty map
func TestIndexGitHubRepositoriesByOrg_empty(t *testing.T) {
    var repos []*GitHubRepository

    result := IndexGitHubRepositoriesByOrg(repos)

    if k := len(result); k != 0 {
        t.Errorf("expected result map to have zero keys, but it has %d keys", k)
    }
}
