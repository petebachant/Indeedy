# -*- coding: utf-8 -*-
"""
This module contains utilities for performing automated searches on Indeed.com

@author: Pete Bachant (petebachant@gmail.com)
"""
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import numpy as np
import matplotlib.pyplot as plt

# Sample variables to consider
cad = ["SolidWorks",
       "Catia",
       "Pro/ENGINEER",
       "Creo",
       "Unigraphics",
       "NX",
       "Inventor"]
language = ["Python",
            "C",
            "Java",
            "MATLAB",
            "LabVIEW",
            "FORTRAN"]
degree = ["BS",
          "MS",
          "PhD"]
cfd = ["OpenFOAM",
       "Fluent",
       "COMSOL",
       "SolidWorks Flow Simulation"]
welding = ["MIG",
           "TIG",
           "stick"]
           
locations = ["Anywhere", "MA", "CA", "KS", "TX", "NH", "Hawaii"]

def find_jobs(job, location=""):
    """This function searches Indeed.com and returns the number of results."""
    job_url = "+".join(job.split())
    job_url = job_url.replace("/", "%2F")
    loc_url = "+".join(location.split())
    loc_url = loc_url.replace(",", "%2C")
    url = "http://www.indeed.com/jobs?q=" + job_url + "&l=" + loc_url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    line = soup.find("meta", {"name":"description"})['content']
    njobs = line.split()[0].replace(",", "")
    try:
        njobs = int(njobs)
    except ValueError:
        njobs = 0
    return njobs
    
def find_salary(job, location=""):
    """Finds average salary for a job search."""
    job_url = "+".join(job.split())
    job_url = job_url.replace("/", "%2F")
    loc_url = "+".join(location.split())
    loc_url = loc_url.replace(",", "%2C")
    url_sal = "http://www.indeed.com/salary?q1=" + job_url + "&l1=" + loc_url
    soup_sal = BeautifulSoup(urllib2.urlopen(url_sal).read())
    line_sal = soup_sal.find("meta", {"name":"description"})['content']
    salary = re.findall("\d+\,\d+", line_sal)[0].replace(",", "")
    try:
        salary = float(salary)
    except ValueError:
        salary = None
    return salary
    
def compare_jobs_title(variable, constant="", location=""):
    """Searches for jobs with one variable and one constant. For example
    constant could be "mechanical engineer" and variable could be a list of
    CAD software names."""
    njobs = np.zeros(len(variable), dtype=int)
    salaries = np.zeros(len(variable))
    for n in range(len(variable)):
        job = constant + " " + variable[n]
        njobs[n] = find_jobs(job, location)
        salaries[n] = find_salary(job, location)
    return njobs, salaries

def compare_jobs_loc(job, locations, plot=False):
    """Searches for jobs throughout a list of locations."""
    njobs = np.zeros(len(locations), dtype=int)
    salaries = np.zeros(len(locations))
    for n in range(len(locations)):
        njobs[n] = find_jobs(job, locations[n])
        salaries[n] = find_salary(job, locations[n])
    return njobs, salaries

def bar_graph(names, quantities, ylabel=""):
    plt.figure(figsize=(12,5))
    plt.bar(range(len(names)), quantities, width=0.5)
    ax = plt.gca()
    ax.set_xticks(np.arange(len(names))+0.25)
    ax.set_xticklabels(names)
    plt.ylabel(ylabel)
    plt.show()
    
def dual_bar_graph(names, njobs, salaries):
    """Makes a bar graph. With both number of jobs and their salaries"""
    plt.figure(figsize=(10,5))
    plt.bar(range(len(names)), njobs, width=0.25)
    ax = plt.gca()
    ax.set_xticks(np.arange(len(names))+0.25)
    ax.set_xticklabels(names)
    ax.tick_params(axis='y', colors='b')
    plt.ylabel("Number of results", color="b")
    ax1 = ax.twinx()
    ax1.bar(np.arange(len(names))+0.25, salaries, width=0.25, color="g")
    ax1.set_ylabel("Average salary (USD)", color="g")
    ax1.tick_params(axis='y', colors='g')
    plt.show()

if __name__ == "__main__":
    import matplotlib
    matplotlib.rcParams["font.family"] = "serif"
    matplotlib.rcParams["font.size"] = 14.0
    plt.close("all")
#    print find_jobs("welder", location="")
#    print find_salary("welder")
    njobs, salaries = compare_jobs_title(cad, constant="mechanical engineer",
                                         location="")
#    njobs, salaries = compare_jobs_loc("mechanical engineer", locations)
    dual_bar_graph(cad, njobs, salaries)