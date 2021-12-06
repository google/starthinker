###########################################################################
#
#  Copyright 2021 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import argparse
import textwrap
import github
import datetime


STAT_HEADER = '  {:<20} {:>10} {:>10} {:>10} {:>10} {:>10}'
STAT_ROW = '  {metric:<20} {daily:>10.1f} {weekly:>10.1f} {monthly:>10.1f} {annual:>10.0f} {total:>10.0f}'
REF_HEADER = '  {:<40} {:>10} {:>10}'
REF_ROW = '  {referrer:<40} {count:>10.0f} {uniques:>10.0f}'
PAGE_HEADER = '  {:<80} {:>10} {:>10}'
PAGE_ROW = '  {page:<80} {count:>10.0f} {uniques:>10.0f}'


def main():

  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Download statistics for a github repository.

    Data is extrapolated to monthly and annnual based on current trends.
    Argument for extrapolation: It gives a picture of current trends across metrics.
    Argument against extrapolation: It does not factor in acceleration.
    Chosen becuase it does not require storing data but gives comparable metrics.

    Examples:
      - python gitgub_stats.py iouehrfkljsah29hrkaf google/starthinker google/alligator2

  """))

  parser.add_argument('token', help='Personal access token.')
  parser.add_argument('repos', nargs='+', help='One or more repo URL minus https://github.com/.')
  args = parser.parse_args()

  git = github.Github(args.token)
  for repo in args.repos:
    repository = git.get_repo(repo)
    age_days = (datetime.datetime.today() - repository.created_at).days

    print()
    print(repo)
    print()
    print(STAT_HEADER.format(
      "Metric",
      "Daily",
      "Weekly",
      "Monthly",
      "Annual",
      "Total"
    ))

    print(STAT_HEADER.format(
      "--------------------",
      "----------",
      "----------",
      "----------",
      "----------",
      "----------",
    ))

    views = repository.get_views_traffic()
    print(STAT_ROW.format(
      metric = 'Views',
      daily = views['count'] / 14, # 14 day total returned
      weekly = views['count'] / 2,
      monthly = views['count'] * 2,
      annual = views['count'] * 2 * 12,
      total = views['count'] / 14 * age_days / 2
    ))

    print(STAT_ROW.format(
      metric = 'Views Unique',
      daily = views['uniques'] / 14, # 14 day total returned
      weekly = views['uniques'] / 2,
      monthly = views['uniques'] * 2,
      annual = views['uniques'] * 2 * 12,
      total = views['uniques'] / 14 * age_days / 2 # attempt liner regression from zero
    ))

    clones = repository.get_clones_traffic()
    print(STAT_ROW.format(
      metric = 'Clones',
      daily = clones['count'] / 14, # 14 day total returned
      weekly = clones['count'] / 2,
      monthly = clones['count'] * 2,
      annual = clones['count'] * 2 * 12,
      total = clones['count'] / 14 * age_days / 2  # attempt liner regression from zero
    ))

    print(STAT_ROW.format(
      metric = 'Clones Unique',
      daily = clones['uniques'] / 14, # 14 day total returned
      weekly = clones['uniques'] / 2,
      monthly = clones['uniques'] * 2,
      annual = clones['uniques'] * 2 * 12,
      total = clones['uniques'] / 14 * age_days / 2 # attempt liner regression from zero
    ))

    stars = repository.stargazers_count
    print(STAT_ROW.format(
      metric = 'Stars',
      daily = stars / age_days,
      weekly = stars / age_days * 7,
      monthly = stars / age_days * 30.5,
      annual = stars / age_days * 365,
      total = stars # total is returned
    ))

    forks = repository.forks_count
    print(STAT_ROW.format(
      metric = 'Forks',
      daily = forks / age_days,
      weekly = forks / age_days * 7,
      monthly = forks / age_days * 30.5,
      annual = forks / age_days * 365,
      total = forks # total is returned
    ))

    subscribers = repository.subscribers_count
    print(STAT_ROW.format(
      metric = 'Subscribers',
      daily = subscribers / age_days,
      weekly = subscribers / age_days * 7,
      monthly = subscribers / age_days * 30.5,
      annual = subscribers / age_days * 365,
      total = subscribers # total is returned
    ))

    watchers = repository.watchers
    print(STAT_ROW.format(
      metric = 'Watchers',
      daily = watchers / age_days,
      weekly = watchers / age_days * 7,
      monthly = watchers / age_days * 30.5,
      annual = watchers / age_days * 365,
      total = watchers # total is returned
    ))

    pulls = len(list(repository.get_pulls(state='all', sort='created', base='master')))
    print(STAT_ROW.format(
      metric = 'Pulls',
      daily = pulls / age_days,
      weekly = pulls / age_days * 7,
      monthly = pulls / age_days * 30.5,
      annual = pulls / age_days * 365,
      total = pulls   # total is returned
    ))

    commits = sum(repository.get_stats_participation().all)
    print(STAT_ROW.format(
      metric = 'Commits (Past Year)',
      daily = commits / min(age_days, 365),
      weekly = commits / min(age_days, 365) * 7,
      monthly = commits / min(age_days, 365) * 30.5,
      annual = commits / min(age_days, 365) * 365,
      total = commits   # only past year is returned ( note in metric )
    ))

    loc = sum(c.additions for c in repository.get_stats_code_frequency())
    print(STAT_ROW.format(
      metric = 'Lines Of Code',
      daily = loc / age_days,
      weekly = loc / age_days * 7,
      monthly = loc / age_days * 30.5,
      annual = loc / age_days * 365,
      total = loc   # only past year is returned ( note in metric )
    ))

    print()
    print(PAGE_HEADER.format(
      "Page",
      "Views",
      "Uniques"
    ))

    print(PAGE_HEADER.format(
      "--------------------------------------------------------------------------------",
      "----------",
      "----------",
    ))

    paths = repository.get_top_paths()
    for path in paths:
      print(PAGE_ROW.format(
        page = path.path.replace(repo + '/', ''),
        count = path.count,
        uniques =  path.uniques
      ))

    print()
    print(REF_HEADER.format(
      "Reference",
      "Views",
      "Uniques"
    ))

    print(REF_HEADER.format(
      "----------------------------------------",
      "----------",
      "----------",
    ))

    referrers = repository.get_top_referrers()
    for referrer in referrers:
      print(REF_ROW.format(
        referrer = referrer.referrer,
        count = referrer.count,
        uniques = referrer.uniques
      ))

    print()

if __name__ == '__main__':
  main()
