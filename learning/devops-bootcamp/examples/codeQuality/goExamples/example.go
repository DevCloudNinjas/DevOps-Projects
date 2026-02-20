package go_unit_test_bootcamp

type GitHubRepository struct {
    Organization string
    Repository   string
    Url          string
    License      string
}

func IndexGitHubRepositoriesByOrg(repos []*GitHubRepository) map[string][]*GitHubRepository {
    result := make(map[string][]*GitHubRepository)

    for _, repo := range repos {
        result[repo.Organization] = append(result[repo.Organization], repo)
    }

    return result
}
